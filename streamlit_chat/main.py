import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)


def init():
    load_dotenv(
        dotenv_path="/Users/ivanzhirnov/Downloads/ds_related/projects/langchain-experiments/.env"
    )
    # Load the OpenAI key from the .env file
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(
        page_title="Chat App",
        page_icon="🧞‍♂️",
    )


def main():
    init()

    chat = ChatOpenAI(temperature=0)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(
                content="You are a helpful personal assistant.",
            ),
        ]

    st.header("Chat App 💬")

    with st.sidebar:
        user_input = st.text_input("Enter your message: ", key="user_input")

        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Processing..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))

    messages = st.session_state.get("messages", [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + "_user")
        else:
            message(msg.content, is_user=False, key=str(i) + "_ai")


if __name__ == "__main__":
    main()
