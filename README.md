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
<img width="1344" height="729" alt="image" src="https://github.com/user-attachments/assets/dc00cbca-ce5d-4a21-a9f4-1068999f2717" />

Connect first the chat input to our AI Agent.
<img width="1344" height="729" alt="image" src="https://github.com/user-attachments/assets/83d46445-fb2f-400a-89e1-4086451588f3" />

> [!IMPORTANT]  
> At this point, you cannot chat with your AI Agent. It is able to read your text, but not to understand it, as we didn't connect the LLM yet.


&nbsp;

## 2. 🧠 Connect the LLM

> [!NOTE]  
> I've decided to use Mistral AI because APIs are free for testing. You can use whatever LLM you have (OpenAI, Anthropic, ...).

To connect the LLM to the AI Agent, we will use APIs. It means that we need an API token for the authentication. For Mistral, all the steps are available here: https://docs.mistral.ai/getting-started/quickstart

At this point, you should have generated your Mistral token:
<img width="1344" height="729" alt="image" src="https://github.com/user-attachments/assets/68a7c572-8d33-4ad1-8b98-e38d3795718a" />

In N8N, add this token into the Mistral LLM node.
<img width="1344" height="729" alt="image" src="https://github.com/user-attachments/assets/4ffbb899-3eb7-4214-b4ba-f4fe8853f1cc" />

Finally, connect the Mistral LLM node to the AI Agent.
<img width="1344" height="729" alt="image" src="https://github.com/user-attachments/assets/1e3f0473-7409-4377-b4f9-2aea4e30fabb" />

> [!IMPORTANT]  
> At this point, you can use the integrated chat of N8N to talk to your AI Agent. However, the AI Agent is just a chatbot, as it doesn't have access to our tools yet.

&nbsp;

## 3. 🛠️ Build the Tool

> [!NOTE]  
> I am using ThousandEyes and Meraki for my tool but you can use any other solutions.

We are using three API calls for this tool:
1. https://developer.cisco.com/docs/thousandeyes/list-active-alerts/
2. https://developer.cisco.com/docs/thousandeyes/retrieve-alert-details/
3. https://developer.cisco.com/meraki/api-v1/get-organization-configuration-changes/

> [!TIP]  
> I highly recommend to use [uv](https://docs.astral.sh/uv/) for package and project management

To run the MCP server, first create a config file name `config.yml`in `tools`folder, and fill it with your values.

```
# ThousandEyes-Meraki Correlation Server Configuration
# Copy this file to config.yml and fill in your actual values

# Server settings
server:
  name: "ThousandEyes-Meraki Correlation"
  host: "your_host_ip_here"  # Host to bind the server to
  port: 42100            # Port to listen on, use whatever you want

# Meraki API configuration
meraki:
  api_key: "your_meraki_api_key_here"
  org_id: "your_org_id_here"
  base_url: "https://api.meraki.com/api/v1"  # Optional: override API base URL

# ThousandEyes API configuration
thousandeyes:
  token: "your_thousandeyes_token_here"
  base_url: "https://api.thousandeyes.com/v7"  # Optional: override API base URL
```

Run the MCP server:
```
uv run mcp_server.py 
```
<img width="1038" height="382" alt="image" src="https://github.com/user-attachments/assets/ebf3faa8-e528-4b89-9057-fa1ae3c71b62" />

You can also create your own MCP server, by copying the file `mcp_server.py` and creating another MCP server. Then add your own scripts / functions in it, and declare it as a tool. You can follow the instructions here : https://gofastmcp.com/getting-started/welcome.

When the MCP server is working as expected (giving the right output), a good practice is then to put it as a Docker. You can check the Dockerfile in the repo.

To do this, create your image from the Dockerfile
```
sudo docker build -t thousandeyes-meraki-mcp .
```
CHeck that your image is properly built
```
sudo docker image ls
REPOSITORY                TAG       IMAGE ID       CREATED        SIZE
thousandeyes-meraki-mcp   latest    c58442a67734   6 days ago     258MB
```

Then run a docker with your image
```
sudo docker run -p 42104:42104 thousandeyes-meraki-mcp
```

<img width="1038" height="382" alt="image" src="https://github.com/user-attachments/assets/78b91715-fc0a-4f75-a54d-b2894bf8437e" />

You now need to configure your MCP client on N8N. Your MCP server should be reachable from your N8N docker. To expose my tool, I am using Cloudflare Tunnels (free), that handles ZTNA access and the HTTPS certificates for me.
<img width="1344" height="729" alt="image" src="https://github.com/user-attachments/assets/f68362ab-6456-4686-b5cd-4f93e017c8d9" />


Once your MCP server is reachable from your N8N, configure your MCP client.
<img width="1344" height="729" alt="image" src="https://github.com/user-attachments/assets/e181e913-d2fd-4060-8e1b-8d0dda0ac289" />


Connect the MCP client node to your AI Agent.
<img width="1344" height="729" alt="image" src="https://github.com/user-attachments/assets/78339b93-f713-481d-8e9b-728c3d095170" />


> [!IMPORTANT]  
> At this point, your AI Agent is working and can perform actions based on chat input. We now need to optimize it.

## 4. 📊 Optimize (Prompting) 

We have a working AI Agent. But we now need to optimize it.

The first optimization can be done via prompting. You need to tell to your AI Agent what is its role, what are its instrutions, and provide some examples of output.

The prompt I was using for the Cisco Live session demo was this one:
```
Role :

You are a Networking Expert correlating ThousandEyes Alerts with Meraki configuration changes.

Instructions :

1. When asked, provide an Root Cause Analysis via MCP tool correlate_alerts_with_meraki_changes, and use the knowledge base to have context on the alert :

### Title : RCA of (20 words max)

**Description:**
___
(what is the issue and time in 20 words max)

**Root cause:**
(what causes the description in 30 words max, quote time if possible, use knowledge base if relevant)

**Scope:**
(x users / x applications)

**Actions plan:**
(high level steps, no details, ask if the user wants detail on how to revert the change)

2. When asked for Meraki implementation guidance, use only data from the knowledge base and tag the document used
```
Then, here are some ways to optimize your AI Agent:

<img width="851" height="477" alt="image" src="https://github.com/user-attachments/assets/6c8ad800-c4b7-4a32-8ace-dcf884708535" />
