import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
import os
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console

load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

model_client=OpenAIChatCompletionClient(model='gpt-4o')


assistant=AssistantAgent(
    name="Assistant_Agent",
    model_client=model_client,
    description="You are a very helpful assistant.",
    system_message="You are a very helpful assistant who help on the task given."
)

user_proxy_agent=UserProxyAgent(
    name="User_proxy_agent",
    description="You are a user proxy agent.",
    input_func=input
)


termination_condition=TextMentionTermination(text="APPROVE")

teams=RoundRobinGroupChat(participants=[assistant,user_proxy_agent],max_turns=10,termination_condition=termination_condition)

stream=teams.run_stream(task=input("Tell me How can I help you:"))

async def main():
    await teams.reset()
    await Console(stream=stream)

if (__name__=='__main__'):
    asyncio.run(main())
