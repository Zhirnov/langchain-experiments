from dotenv import load_dotenv
import streamlit as st
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
import qdrant_client
import os
from langchain.document_loaders import PyPDFLoader


def get_vector_store():
    client = qdrant_client.QdrantClient(
        os.getenv("QDRANT_HOST"), 
        api_key=os.getenv("QDRANT_API")
    )
    embeddings = OpenAIEmbeddings()

    # Initialize vector store object

    vector_store = Qdrant(
        client=client,
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
        embeddings=embeddings,
    )

    return vector_store


def main():
    load_dotenv()
    st.set_page_config(page_title="Query your data from Qdrant")
    st.header("Access to remote database 🗨️")

    # Create vector store
    vector_store = get_vector_store()

    # Create a chain
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=vector_store.as_retriever()
    )

    # User input
    user_question = st.text_input("Write your question related to database:")
    if user_question:
        st.write(f"Question: {user_question}")
        answer = qa.run(user_question)
        st.write(f"Response: {answer}")


if __name__ == "__main__":
    main()
