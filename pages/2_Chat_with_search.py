
import streamlit as st

from langchain.agents import initialize_agent, AgentType, Tool
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import AzureChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory


key1 = st.secrets["key1"]

 
st.title("🧐 Dr.DuckDuck")



if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="The best places in the world for ducks"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

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


    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
