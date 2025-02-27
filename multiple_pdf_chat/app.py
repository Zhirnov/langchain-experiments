import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(raw_text):
    splitter = RecursiveCharacterTextSplitter(
        # separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    text_chunks = splitter.split_text(raw_text)
    return text_chunks


def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store


def get_conversation_chain(vector_store):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(
    #     repo_id="google/flan-t5-xl",
    #     model_kwargs={"temperature": 0.5, "max_length": 512},
    # )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory,
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(
                user_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True,
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True
            )


def main():
    load_dotenv(
        "/Users/ivanzhirnov/Downloads/ds_related/projects/langchain-experiments/.env"
    )

    st.set_page_config(page_title="Ask your data", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Ask your data :books:")
    user_question = st.text_input("Type in your question:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Docs")
        pdf_docs = st.file_uploader("Upload your docs here", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                # Get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # Get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # Create vector store
                vector_store = get_vector_store(text_chunks)

                # Create conversation chain
                st.session_state.conversation = get_conversation_chain(vector_store)


if __name__ == "__main__":
    main()
