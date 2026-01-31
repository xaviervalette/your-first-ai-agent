> [!IMPORTANT]  
> This lab follows the Cisco Live session AI-1707 where we designed your first AI Agent. Now we are building this AI Agent. I recommend to check the Cisco Live materials if you didn't already


# Build Your First AI Agent

| Step | Time |
| :---         |     :---:      |
| 0. 🔎 Lab overview   | `30min`     |
| 1. 🤖 Install the AI Agent Framework (N8N)     | `30min`       |
| 2. 🧠 Connect the LLM (Mistral AI Large 3)     | `30min`       |
| 3. 🛠️ Build the tools (MCP)     | `1h`      |
| 4. 📊 Optimize (Prompting)     | `30min`       |

&nbsp;

## 0. 🔎 Lab overview

### Lab structure

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

### Lab architecture
<img width="915" height="409" alt="image" src="https://github.com/user-attachments/assets/0305fb7e-f0a2-4521-88e0-c4bcf572c2fa" />



### Lab requirements
- Docker
- Meraki and ThousandEyes APIs (or any other solutions)
- Mistral AI API (or any other LLM)
- Python and uv

&nbsp;

## 1. 🤖 Install the AI Agent Framework (N8N) - 30min

> [!NOTE]  
> I have a Intel NUC for lab purposes, so I decided to use the On-Premise deployment via Docker to reduce costs, but N8N can be use as SaaS, in Public Cloud or On-Premise.


To install the N8N Docker, I recommend to use `docker-compose`.

```
cd n8n
sudo docker-compose up
```

After few seconds, you should be able to connect to 'http://your-host-ip:5678':
<img width="1344" height="729" alt="image" src="https://github.com/user-attachments/assets/d4848201-6241-463b-b4f5-d969517eef94" />


Follow the instruction to create an account.

Once the N8N application is setup, create a first workflow and copy+paste the content of 'your_first_ai_agent_n8n_workflow.json':

You should have the following result:

<img width="454" height="277" alt="image" src="https://github.com/user-attachments/assets/1d53c13f-6834-4893-90d2-65eb7fbecd29" />

&nbsp;

## 2. 🧠 Connect the LLM

> [!NOTE]  
> I've decided to use Mistral AI because APIs are free for testing. You can use whatever LLM you have (OpenAI, Anthropic, ...).

To connect the LLM to the AI Agent, we will use APIs. It means that we need an API token for the authentication. For Mistral, all the steps are available here: https://docs.mistral.ai/getting-started/quickstart

At this point, you should have generated your Mistral token:
<img width="1418" height="580" alt="image" src="https://github.com/user-attachments/assets/d4ec4d9c-92d5-4a96-824e-fdb6ab1ac7a3" />

In N8N, add this token into the Mistral LLM node.
<img width="1344" height="1162" alt="image" src="https://github.com/user-attachments/assets/16036e7e-0e0c-4a09-9c7a-0e583376c3a2" />


&nbsp;

## 3. 🛠️ Build the Tool

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

