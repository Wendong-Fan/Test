
import streamlit as st

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import AzureChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from PIL import Image

key1 = st.secrets["key1"]

 
st.title("🧐 Dr.DuckDuck")
#image0 = Image.open('images.jpeg')
#st.image(image0)


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
 
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
