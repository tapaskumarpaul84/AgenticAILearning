from autogen_agentchat.agents import AssistantAgent
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from autogen_ext.tools.http import HttpTool
from dotenv import load_dotenv
import os

load_dotenv()

try:
    os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
except Exception as e:
    print("Please provide a valid api key")

model_client=OpenAIChatCompletionClient(model='gpt-4o')

schema={
    "type": "object",
    "properties": {
        "fact": {
            "type": "string",
            "description": "a random cat fact"
                },
        "length": {
            "type": "integer",
            "description": "Length of the cat fact"

        }
    },
    "required": ["fact","length"],
}

# Create an HTTP tool for the httpbin API
http_tool = HttpTool(
    name="cat_facts_api_tool",
    description="get a cool cat fact",
    scheme="https",
    host="https://catfact.ninja/",
    port=443,
    path="/fact",
    method="GET",
    return_type="json",
    json_schema=schema,
)



agent=AssistantAgent(
    name="Cat_fact_assistant",
    model_client=model_client,
    system_message="You are a helpful assistant to provide a cat fact with a cool manner, " \
    "provide the summary of the fact.",
    tools=[http_tool],
    reflect_on_tool_use=True
)


async def main():
    result= await agent.run(task="please provide a cat fact.")
    print(result.messages[-1].content)

if (__name__)=="__main__":
    asyncio.run(main())