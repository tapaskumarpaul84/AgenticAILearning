import asyncio
import os
from dotenv import load_dotenv
import time
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench,StdioServerParams

load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
async def main():
    params=StdioServerParams(
        command='uvx',
        args=['mcp-server-time','--local-timezone=America/New_York']
    ) 

    model_client=OpenAIChatCompletionClient(model='gpt-4o')

    async with McpWorkbench(server_params=params) as workbench:
        agent=AssistantAgent(
            name="Agent",
            system_message="You are a helpful assistant.",
            model_client=model_client,
            workbench=workbench,
            reflect_on_tool_use=True
        )

        task="What is the current time in London?"
        async for message in agent.run_stream(task=task):
            print("***********************************")
            print(message)
            print("####################################")


if __name__=='__main__':
    asyncio.run(main())

