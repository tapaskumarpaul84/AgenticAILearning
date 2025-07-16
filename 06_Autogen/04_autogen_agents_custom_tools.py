import asyncio
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

try:
    os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
except Exception as e:
    print("Please provide a valid api key")

model_client=OpenAIChatCompletionClient(model='gpt-4o')

def reverse_string(text: str)-> str:
    """
    Reverse the given string.
    input: str

    output: str

    The reversed string is returned.
    """
    return text[::-1]

reverse_tool=FunctionTool(reverse_string,description="A tool to reverse a string.") #FunctionTool is a wrapper to make the function as Basemodel tools


agent=AssistantAgent(
    name="ReverseAssistantAgent",
    model_client=model_client,
    system_message="""You are a helpful assistant that can reverse string using reverse_string tool.Provide the result with the execution summary.""", # instructions to the brain(LLM)
    tools=[reverse_tool], #can be multiple tools
    reflect_on_tool_use=True # with tool call details and use brain on tool response, if False return tool response only
    )

async def main():
    result=await agent.run(task="Please reverse the string 'Hello World!'")
    #print(result) #complete response
    print(result.messages[-1].content)

if (__name__=="__main__"):
    asyncio.run(main())
    