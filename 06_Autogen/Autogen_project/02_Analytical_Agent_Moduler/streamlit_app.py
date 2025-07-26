import streamlit as st
import asyncio
import os
from teams.analyzer_team import getDataAnalyzerTeam
from models.openai_model import get_model_client
from config.docker_utils import getDockerCommandLineExecutor,start_docker_container,stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

st.title('Analyzer Agent - Digital Data Analyst')
uploaded_file=st.file_uploader("Upload a csv file",type=['csv'])

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state = None
if('images_shown') not in st.session_state:
    st.session_state.images_shown=[]

task=st.chat_input("Enter your task here....")

async def run_analyzer_agent(docker,openai_model_client,task):
    try:
        await start_docker_container(docker=docker)
        teams=getDataAnalyzerTeam(docker=docker,model_client=openai_model_client)
        if st.session_state.autogen_team_state is not None:
            await teams.load_state(st.session_state.autogen_team_state)
        async for message in teams.run_stream(task=task):
            #st.markdown(f"{message}")
            if isinstance(message,TextMessage):
                if message.source.startswith('user'):
                    with st.chat_message('user',avatar='👤'):
                        st.markdown(message.content)
                elif message.source.startswith('Data_Analyzer_Agent'):
                    with st.chat_message('Data Analyzer',avatar='🤖'):
                        st.markdown(message.content)
                elif message.source.startswith('Python_code_executor'):
                    with st.chat_message('Code Executor',avatar='👨‍💻'):
                        st.markdown(message.content)
            elif isinstance(message,TaskResult):
                st.markdown(f'Stop Reason: {message.stop_reason}')
                st.session_state.messages.append(message.stop_reason)
        st.session_state.autogen_team_state = await teams.save_state()
        return None
    except Exception as e:
        st.error(f"Error Occured: {e}")
        return e
    finally:
        await stop_docker_container(docker=docker)

if st.session_state.messages:
    for msg in st.session_state.messages:
        st.markdown(msg)


if task:
    if uploaded_file is not None:
        if not os.path.exists('temp'):
            os.makedirs('temp',exist_ok=True)

        with open('temp/data.csv','wb') as f:
            f.write(uploaded_file.getbuffer())

        openai_model_client=get_model_client()
        docker=getDockerCommandLineExecutor()

        error=asyncio.run(run_analyzer_agent(docker,openai_model_client,task))

        if error:
            st.error(f'An error occured: {error}')

        if os.path.exists('temp/output.png'):
            st.image('temp/output.png', caption='Output Image')
    else:
        st.warning('Please upload the file and provide the task.')

