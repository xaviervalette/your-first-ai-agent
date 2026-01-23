# Build Your First AI Agent

A lab guide to Build Your first AI Agent.

This refers to the Cisco Live session AI-1707: "Design And Build Your First AI Agent". In this session, we designed the following AI Agent:
<img width="3973" height="1902" alt="image" src="https://github.com/user-attachments/assets/edd12053-18ac-4dc5-b624-a4c319e5ddbb" />


The choices made in the Design phase were:
- **Input**: The task "Collect ThousandEyes alerts with Meraki configuration changes and summarizes potential causes."
- **Tools**: Cisco ThousandEyes and Cisco Meraki APIs with Model Context Protocols (MCP)
- **LLM**: Gemini 3 Pro
- **AI Agent Framework**: N8N
- **Ouput**: A Root Cause Analysis (RCA)

Here is what we will build now:
IMAGE

We will follow the following steps:
1. 🤖 Install the AI Agent Framework (N8N) - 30min
2. ...
3. ...
4. ...
5. ...

## 1. 🤖 Install the AI Agent Framework (N8N) - 30min

N8N is a very flexible solution in term of deployment options (SaaS, Public Cloud, On-Premise).

I have a Intel NUC for lab purposes, so I decided to use the On-Premise deployment via Docker to reduce costs.

<img width="200" height="" alt="nuc" src="https://github.com/user-attachments/assets/c8f4af0e-9a51-4239-91df-48918a27dc93" />



To install the Docker, I recommend to use `docker-compose`:

```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - GENERIC_TIMEZONE=CET
      - TZ=CET
      - N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true
      - N8N_RUNNERS_ENABLED=true
      - WEBHOOK_URL=https://n8n.xvalette.com/
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
    external: true
```

```
cat docker-compose.yml
```

You should be able to connect to 'http://<your-host-ip>:5678' after few seconds.

Once the N8N application setup, create a first workflow and copy+paste the content of 'your_first_ai_agent_n8n_workflow.json':

You should have the following result:

<img width="454" height="277" alt="image" src="https://github.com/user-attachments/assets/1d53c13f-6834-4893-90d2-65eb7fbecd29" />


## 2. Build the Tool

We are using three API calls for this tool:
1. https://developer.cisco.com/docs/thousandeyes/list-active-alerts/
2. https://developer.cisco.com/docs/thousandeyes/retrieve-alert-details/
3. https://developer.cisco.com/meraki/api-v1/get-organization-configuration-changes/

You can use the code snippets providen by the API website.



Then, build the MCP Server:

```python
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

## 3. The LLM


## 4. The AI Agent

