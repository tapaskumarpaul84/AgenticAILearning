import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams,mcp_server_tools
from autogen_agentchat.conditions import  TextMentionTermination

load_dotenv()
notion_secret=os.getenv("NOTION_SECRET")
openai_api_key=os.getenv("OPENAI_API_KEY")

system_message="""You are a helpful assistant that can search and summerize content from the user's Notion 
workspace and also list what is asked. Try to assume the tool and call the same and get the answer,
say TERMINATE when you done with the task."""

async def config():
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


async def orchestrate(team,task):
    async for msg in team.run_stream(task=task):
        yield msg

async def main():
    team=await config()
    task= "create a new page titled 'PageFromMCPNotion'"
    async for msg in orchestrate(team,task):
        print('*'*100)
        print(msg)
        print('-'*100)

if __name__=="__main__":
    asyncio.run(main())





