import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from langchain_community.utilities import GoogleSerperAPIWrapper

load_dotenv()

try:
    os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
    os.environ["SERPER_API_KEY"]=os.getenv("SERPER_API_KEY")
except Exception as e:
    print("Please provide valid api keys.")


model_client=OpenAIChatCompletionClient(model='gpt-4o')

search_tool=GoogleSerperAPIWrapper(type='news')

def search_web(query : str)-> str:
    """Search the web with the given query and provide the results."""
    try:
        result=search_tool.run(query)
        return result
    except Exception as e:
        print(f"Error occured while searching the web: {e}")
        return "No result found"

my_agent=AssistantAgent(
                name="Web_Assistant",
                model_client=model_client,
                system_message="You are a helpful assistant that can search in the web for informtion using search_web tool." \
                "Please make sure that you use the search_web tool to find out information before you return the answer.",
                tools=[search_web],
                description="A Agent that can search in the Web to provide any response.",
                reflect_on_tool_use=True
                )


async def search_agent(query):
    """Run the my_agent with the simple question."""
    #query="Who won the IPL 2025?"
    print(f"Query: {query}")
    result=await my_agent.run(task=query)
    print(result.messages[-1].content)

if (__name__)=="__main__":
    query="Who won the IPL 2025?"
    asyncio.run(search_agent(query))


