import os
from typing import Any
import httpx
import logging
from mcp.server.fastmcp import FastMCP
import sys
from datetime import datetime, timedelta, timezone
import yaml
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_config(config_path: str = "config.yml") -> dict:
    """Load and validate configuration from YAML file."""
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    config = yaml.safe_load(config_file.open())
    
    # Validate required fields
    for field in ['meraki.api_key', 'meraki.org_id', 'thousandeyes.token']:
        value = config
        for key in field.split('.'):
            if (value := value.get(key)) is None:
                raise ValueError(f"Missing required config field: {field}")
    
    logger.info(f"Configuration loaded from {config_path}")
    return config

# Load configuration and initialize server
try:
    config = load_config()
except Exception as e:
    logger.critical(f"Failed to load configuration: {e}")
    sys.exit(1)

mcp = FastMCP(
    config.get('server', {}).get('name', 'ThousandEyes-Meraki Correlation'),
    host=config.get('server', {}).get('host', '192.168.2.24'),
    port=config.get('server', {}).get('port', 42104),
    stateless_http=True,
)

# API Configuration
MERAKI_API_KEY = config['meraki']['api_key']
MERAKI_ORG_ID = config['meraki']['org_id']
MERAKI_BASE_URL = config['meraki'].get('base_url', 'https://api.meraki.com/api/v1')
THOUSANDEYES_TOKEN = config['thousandeyes']['token']
THOUSANDEYES_BASE_URL = config['thousandeyes'].get('base_url', 'https://api.thousandeyes.com/v7')

def parse_timestamp_to_utc(timestamp_str: str) -> datetime | None:
    """Parse timestamp string and convert to UTC datetime."""
    if not timestamp_str:
        return None
    try:
        timestamp_str = timestamp_str.replace('Z', '+00:00')
        dt = datetime.fromisoformat(timestamp_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception as e:
        logger.warning(f"Failed to parse timestamp '{timestamp_str}': {e}")
        return None

@mcp.tool()
async def correlate_alerts_with_meraki_changes(window_minutes: int = 30) -> dict[str, Any]:
    """
    Correlate ThousandEyes alerts with Meraki configuration changes.
    
    Args:
        window_minutes: Time window in minutes before and after alert (default: 30)
    
    Returns:
        Dictionary containing correlated alerts and Meraki changes
    """
    logger.info("Starting correlation workflow...")
    
    # Fetch active alerts
    headers = {"Authorization": f"Bearer {THOUSANDEYES_TOKEN}", "Accept": "application/hal+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{THOUSANDEYES_BASE_URL}/alerts", headers=headers, timeout=30.0)
            response.raise_for_status()
            alerts = response.json().get("alerts", [])
        except Exception as e:
            return {"success": False, "error": f"Failed to fetch ThousandEyes alerts: {str(e)}"}
    
    if not alerts:
        logger.info("No active alerts found")
        return {"success": True, "message": "No active alerts found", "correlations": []}
    
    logger.info(f"Found {len(alerts)} active alerts")
    correlations = []
    
    # Process each alert
    for alert in alerts:
        alert_id = alert.get("alertId")
        logger.info(f"Processing alert {alert_id}...")
        
        # Get alert details
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{THOUSANDEYES_BASE_URL}/alerts/{alert_id}", headers=headers, timeout=30.0)
                response.raise_for_status()
                alert_detail = response.json()
            except Exception as e:
                logger.warning(f"Failed to get details for alert {alert_id}: {str(e)}")
                continue
        
        # Parse alert time and calculate window
        alert_time = parse_timestamp_to_utc(alert_detail.get("dateStart") or alert.get("dateStart"))
        if not alert_time:
            logger.warning(f"No valid timestamp for alert {alert_id}")
            continue
        
        time_window_start = alert_time - timedelta(minutes=window_minutes)
        time_window_end = alert_time + timedelta(minutes=window_minutes)
        timespan_seconds = min(int((datetime.now(timezone.utc) - time_window_start).total_seconds()), 2592000)
        
        logger.info(f"Fetching Meraki changes for window: {time_window_start} to {time_window_end}")
        
        # Get Meraki changes
        meraki_headers = {"Authorization": f"Bearer {MERAKI_API_KEY}", "Accept": "application/json"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{MERAKI_BASE_URL}/organizations/{MERAKI_ORG_ID}/configurationChanges",
                    headers=meraki_headers,
                    params={"timespan": timespan_seconds, "perPage": 1000},
                    timeout=30.0
                )
                response.raise_for_status()
                all_changes = response.json()
            except Exception as e:
                logger.warning(f"Failed to get Meraki changes for alert {alert_id}: {str(e)}")
                continue
        
        # Filter changes to time window
        filtered_changes = [
            change for change in all_changes
            if (change_time := parse_timestamp_to_utc(change.get("ts")))
            and time_window_start <= change_time <= time_window_end
        ]
        
        logger.info(f"Found {len(filtered_changes)} Meraki changes in time window for alert {alert_id}")
        
        correlations.append({
            "alert_id": alert_id,
            "alert_time": alert_time.isoformat(),
            "alert_details": alert_detail,
            "time_window": {
                "start": time_window_start.isoformat(),
                "end": time_window_end.isoformat(),
                "window_minutes": window_minutes
            },
            "meraki_changes": filtered_changes,
            "changes_count": len(filtered_changes)
        })
    
    return {
        "success": True,
        "total_alerts": len(alerts),
        "correlations_found": len(correlations),
        "correlations": correlations
    }

# Run the server
try:
    mcp.run(transport="streamable-http")
except KeyboardInterrupt:
    logger.info("\n🛑 Server shutting down gracefully...")
    sys.exit(1)
except Exception as e:
    logger.critical(f"❌ A critical error occurred: {e}", exc_info=True)
    sys.exit(1)
finally:
    logger.info("✅ Server exited.")
