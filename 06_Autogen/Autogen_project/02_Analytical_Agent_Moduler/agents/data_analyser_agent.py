from autogen_agentchat.agents import AssistantAgent
from agents.prompts.data_analyzer_messages import DATA_ANALYZER_SYSTEM_MESSAGE


def getDataAnalyzerAgent(model_client):
    data_analyzer_agent=AssistantAgent(
        name="Data_Analyzer_Agent",
        model_client=model_client,
        description="An agent that solves Data Analysis problem and gives the python code for the required analysis.",
        system_message=DATA_ANALYZER_SYSTEM_MESSAGE
    )
    return data_analyzer_agent