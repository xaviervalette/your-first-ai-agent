> [!IMPORTANT]  
> This lab follows the Cisco Live session AI-1707 where we designed your first AI Agent. Now we are building this AI Agent. I recommend to check the Cisco Live materials if you didn't already

# Build Your First AI Agent


## Project Structure

```
.
├── n8n
|   ├── compose.yml
|   └── your_first_ai_agent_n8n_workflow.json
|
├── tools
|   ├── config.example.yml
|   └── mcp_server.py
| 
└── README.md
```

## Project Architecture
TODO

## Project Agenda
We will follow the following steps:
1. 🤖 Install the AI Agent Framework (N8N) - 30min
2. Connect the LLM
3. Build the tools


## Project Requirements
TODO


A lab guide to Build Your first AI Agent.

The choices made in the Design phase were:
- **Input**: The task "Collect ThousandEyes alerts with Meraki configuration changes and summarizes potential causes."
- **Tools**: Cisco ThousandEyes and Cisco Meraki APIs with Model Context Protocols (MCP)
- **LLM**: Gemini 3 Pro
- **AI Agent Framework**: N8N
- **Ouput**: A Root Cause Analysis (RCA)

## 1. 🤖 Install the AI Agent Framework (N8N) - 30min

> [!NOTE]  
> N8N can be use as SaaS, in Public Cloud or On-Premise

I have a Intel NUC for lab purposes, so I decided to use the On-Premise deployment via Docker to reduce costs.

To install the N8N Docker, I recommend to use `docker-compose`.

```
cd n8n
sudo docker-compose up
```

After few seconds, you should be able to connect to 'http://<your-host-ip>:5678'.

Follow the instruction to create an account.

Once the N8N application is setup, create a first workflow and copy+paste the content of 'your_first_ai_agent_n8n_workflow.json':

You should have the following result:

<img width="454" height="277" alt="image" src="https://github.com/user-attachments/assets/1d53c13f-6834-4893-90d2-65eb7fbecd29" />

## 2. Connect the LLM



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

