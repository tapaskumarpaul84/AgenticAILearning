import os
from dotenv import load_dotenv
from flask import Flask,jsonify,request
from pyngrok import ngrok
from flask_cors import CORS
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams,mcp_server_tools
from autogen_agentchat.conditions import  TextMentionTermination


load_dotenv()
NGROK_AUTH_TOKEN=os.getenv("NGROK_AUTH_TOKEN")
notion_secret=os.getenv("NOTION_SECRET")
openai_api_key=os.getenv("OPENAI_API_KEY")
port=7001
system_message="""You are a helpful assistant that can search and summerize content from the user's Notion 
workspace and also list what is asked. Try to assume the tool and call the same and get the answer,
say TERMINATE when you done with the task."""

app=Flask(__name__)
CORS(app)

async def setup_team():
    params=StdioServerParams(
        command='npx',
        args=['-y','mcp-remote','https://mcp.notion.com/mcp'],
        env={'NOTION_API_KEY':notion_secret},
        read_timeout_seconds=30
    )

    model_client=OpenAIChatCompletionClient(
        model='gpt-4o',
        api_key=openai_api_key
    )

    notion_tools=await mcp_server_tools(server_params=params)

    assistant_agent=AssistantAgent(
        name= 'notion_agent',
        model_client=model_client,
        system_message=system_message,
        tools=notion_tools,
        reflect_on_tool_use=True
    )

    team=RoundRobinGroupChat(
        participants=[assistant_agent],
        max_turns=5,
        termination_condition=TextMentionTermination(text='TERMINATE')
    )

    return team


async def run_task(task:str) ->str:
    team= await setup_team()
    output=[]

    async for msg in team.run_stream(task=task):
        output.append(msg)

    return '\n \n \n'.join(output)


######################api building##################

@app.route('/',methods=['GET'])
def root():
    return jsonify({"message":"MCP notion app is live,use /health and /run to work on that"}),str(200)

@app.route('/health',methods=['GET'])
def health():
    return jsonify({"status":"running","message":"MCP Notion is live"}),str(200)

@app.route('/run',methods=['POST'])
def run():
    try:
        data=request.get_json()
        task=data.get('task')

        if not task:
            return jsonify({"message":"missing task"}),400
        print(f"got the task: {task}")

        result=asyncio.run(run_task(task))
        return jsonify({"status":"success","result":result}),str(200)
    except Exception as e:
        return jsonify({"status":"failure","result":str(e)}),500
    

if __name__=="__main__":
    
    ngrok.set_auth_token(token=NGROK_AUTH_TOKEN)
    public_url=ngrok.connect(port)
    print(f"Public url: {public_url}")
    app.run(port=port)