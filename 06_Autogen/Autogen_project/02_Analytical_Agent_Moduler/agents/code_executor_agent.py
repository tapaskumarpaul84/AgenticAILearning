from autogen_agentchat.agents import CodeExecutorAgent

def getCodeExecutorAgent(code_executor):
    executor_agent=CodeExecutorAgent(
        name="Python_code_executor",
        code_executor=code_executor
    )
    return executor_agent