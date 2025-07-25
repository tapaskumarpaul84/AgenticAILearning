from autogen_agentchat.agents import CodeExecutorAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_core import CancellationToken
import asyncio

async def main():
    docker=DockerCommandLineCodeExecutor(
        work_dir='/tmp',
        timeout=120
    )

    code_execute_agent=CodeExecutorAgent(
        name="CodeExecutorAgent",
        code_executor=docker
    )

    task=TextMessage(
        content='''
Here is the python code.
```python
print("Hello world!")
print(5+8)
```
''',
    source='user'
    )

    await docker.start()

    result=await code_execute_agent.on_messages(messages=[task],
                                          cancellation_token=CancellationToken())
    print(result.chat_message)

    await docker.stop()

if (__name__=='__main__'):
    asyncio.run(main())