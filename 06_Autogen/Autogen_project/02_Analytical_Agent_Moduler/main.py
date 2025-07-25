from autogen_agentchat.messages import TextMessage
from teams.analyzer_team import getDataAnalyzerTeam
from models.openai_model import get_model_client
from config.docker_utils import getDockerCommandLineExecutor,start_docker_container,stop_docker_container
import asyncio

async def main():

    openai_model_client=get_model_client()
    docker=getDockerCommandLineExecutor()

    team=getDataAnalyzerTeam(docker=docker,model_client=openai_model_client)

    try:
        task='can you give me a graph of flower types with count in data iris.csv'

        await start_docker_container(docker=docker)
        async for message in team.run_stream(task=task):
            print(message)

    except Exception as e:
        print(e)
    finally:
        await stop_docker_container(docker=docker)


if (__name__=='__main__'):
    asyncio.run(main())