from codecs import StreamReader
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from dotenv import load_dotenv
import os
from autogen_agentchat.ui import Console

load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

brain=OpenAIChatCompletionClient(model='gpt-4o')


assistant1=AssistantAgent(
    name='Writer',
    model_client=brain,
    description='Writer who can write something about the given input',
    system_message='You are a writer who can easily write on the given topic.write less than 30 words.'
)

assistant2=AssistantAgent(
    name='Reviewer',
    model_client=brain,
    description='Review the output from the previous run.',
    system_message='You are a reviewer who can review the previous run output. write less than 30 words.'
)

assistant3=AssistantAgent(
    name='Editor',
    model_client=brain,
    description='Editor who can edit the text',
    system_message='You are a helpful editor who can edit and write less than 30 words.'
)

#teams=RoundRobinGroupChat(participants=[assistant1,assistant2,assistant3],max_turns=3)
teams=RoundRobinGroupChat(participants=[assistant1,assistant2,assistant3],max_turns=1)
async def main():
    #task="Write a 3 lines of poem on sky."
    task=input("Tell me how can I help you?")
    while True:
        stream=teams.run_stream(task=task)
        await Console(stream=stream)

        feedback_from_user_app=input("Please provide your feedback:")
        if feedback_from_user_app.lower().strip()=='exit':
            break
        task=feedback_from_user_app

if (__name__=="__main__"):
    asyncio.run(main())

