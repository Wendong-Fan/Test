import streamlit as st

from langchain.agents import initialize_agent, AgentType, Tool
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import AzureChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory


key1 = st.secrets["key1"]

llm = AzureChatOpenAI(
                openai_api_base = "https://azureopenai-mutiagent.openai.azure.com/",
                openai_api_version = "2023-03-15-preview",
                openai_api_key = key1,
                openai_api_type = "azure",
                deployment_name="gpt-35-turbo",
                model_name="gpt-35-turbo", 
                streaming=True)

duck_search = DuckDuckGoSearchRun()

tools = [
Tool(
    name = "DuckDuckGoSearch",
    func = duck_search.run,
    description = "useful when you need to answer questions that you don't know"
)
]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

search_agent = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True
                            , memory=memory)

 
st.title("🧐 Dr.DuckDuck")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in search_agent.run(prompt):
            full_response += response
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
