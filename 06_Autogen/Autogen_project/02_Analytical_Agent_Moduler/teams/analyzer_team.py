from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.code_executor_agent import getCodeExecutorAgent
from agents.data_analyser_agent import getDataAnalyzerAgent
from config.constants import TERMINATION_MESSAGE,MAX_TRUNS

def getDataAnalyzerTeam(docker,model_client):
    code_executor_agent=getCodeExecutorAgent(code_executor=docker)
    data_analyzer_agent=getDataAnalyzerAgent(model_client=model_client)

    text_mention_termination=TextMentionTermination(TERMINATION_MESSAGE)

    team=RoundRobinGroupChat(
        participants=[data_analyzer_agent,code_executor_agent],
        termination_condition=text_mention_termination,
        max_turns=MAX_TRUNS
    )

    return team