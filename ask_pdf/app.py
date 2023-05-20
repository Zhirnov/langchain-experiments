from io import StringIO, BytesIO
from dotenv import load_dotenv
import tempfile, os

# Import OpenAI as main LLM service
from langchain.llms import OpenAI

# Bring in streamlit for UI/app interface
import streamlit as st

# Import PDF reader for reading PDFs
from langchain.document_loaders import PyPDFLoader, OnlinePDFLoader
from PyPDF2 import PdfReader, PdfWriter

# Import chroma as the vector store
from langchain.vectorstores import Chroma

# Import vector store stuff
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo,
)
from langchain.text_splitter import CharacterTextSplitter


load_dotenv(
    dotenv_path="/Users/ivanzhirnov/Downloads/ds_related/projects/langchain-experiments/.env"
)
# Create a new LLM instance
llm = OpenAI(temperature=0.9)

st.set_page_config(
    page_title="Ask your PDF",
)
st.header("Ask your PDF")

user_pdf = st.file_uploader("Upload your PDF", type="pdf")

if user_pdf is not None:
    # Save the uploaded PDF as a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(user_pdf.read())
        temp_file_path = temp_file.name

    # Load from pdf
    loader = PyPDFLoader(temp_file_path)
    # Split pages from pdf
    pages = loader.load_and_split()
    # Load docs into vector database aka ChromaDB
    store = Chroma.from_documents(pages, collection_name="pdf_pages")

    # Remove the temporary file
    if temp_file_path:
        os.remove(temp_file_path)

    # Create vectorstore info object - metadata repo
    vectorstore_info = VectorStoreInfo(
        name="pdf_pages", description="PDF pages", vectorstore=store
    )

    # Convert the documents store into a langchain toolkit
    toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)

    # Add the toolkit to an end-to-end LC
    agent_executor = create_vectorstore_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
    )

    # Create a text input box for the user to type in
    prompt = st.text_input("Enter your text here")

    # If the user has entered text, then run the model
    if prompt:
        # Pass the prompt to the model
        # answer = llm(prompt)
        # Swap out the raw llm for a document agent
        answer = agent_executor.run(prompt)
        # Print the answer
        st.write(answer)

        # With a streamlit expander
        with st.expander("Document Similarity Search"):
            # Find the relevant pages
            search = store.similarity_search_with_score(prompt)
            # Write out the first
            st.write(search[0][0].page_content)
