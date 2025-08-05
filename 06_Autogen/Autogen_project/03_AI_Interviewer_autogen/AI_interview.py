from autogen_agentchat.agents import AssistantAgent,UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
import asyncio

load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

model_client=OpenAIChatCompletionClient(model='gpt-4o')

job_position="Soft"

##### Define Agents##########

interviewer_agent=AssistantAgent(
    name="Interviewer",
    model_client=model_client,
    description=f"An AI Agent that conducts interviews for a role of {job_position} position.",
    system_message=f"""
    You are a proffessional interviewer for a {job_position} position.
    You ask one question at a time and ask user to provide response and wait for the user response.
    Ask total 5 questions in total for covering technical skill, experience ,problem 
    solving abilities and cultural fit.

    Your job is to ask the question only don't provide any answer or don't pay attention 
    on career_coach responce.

    make sure that you asked question based on candidate's response of previous question 
    and you experise.If the user can able to answer the questions properly make the quite 
    harder else make the question easy.

    
"""
)
#After asking all 5 questions and completing the whole procedure, say 'TERMINATE' at the end of the interview.

candidate_agent=UserProxyAgent(
    name="candidate",
    description=f"An agent that simulates a candidate for a {job_position} role.",
    input_func=input)


career_coach_agent=AssistantAgent(
    name='career_coach',
    model_client=model_client,
    description=f"An AI agent that can provides the feedback and advice to candidates for a {job_position} position.",
    system_message=f"""
    You are a career coach specializing in preparing interviews for the {job_position} 
    position.

    Provide a constractive feedback on the basis of candidate's reponses and suggest the 
    improvements.After providing feedback Interviewer will ask the next question. You only 
    provide the feedback you cannot ask any question.

    After completing the interview , summarize the candidate's performance and provide 
    actionable advices.
    
    After completing the whole task or providing performance details and actionable actions, 
    say 'TERMINATE' at the end of interview.
    """
    )



############Building Team##########

team=RoundRobinGroupChat(
    participants=[interviewer_agent,candidate_agent,career_coach_agent],
    termination_condition=TextMentionTermination(text='TERMINATE'),
    max_turns=20
)


stream=team.run_stream(task="Conducting an interview for a software Engineer position.")

async def main():
    await Console(stream)


if __name__=='__main__':
    asyncio.run(main())

