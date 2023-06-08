import os
from dotenv import load_dotenv, find_dotenv
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import YoutubeLoader
import textwrap

# --------------------------------------------------------------
# Load the HuggingFace Hub API token
# --------------------------------------------------------------

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

# --------------------------------------------------------------
# Load the LLM model from the HuggingFace Hub
# --------------------------------------------------------------

repo_id = "tiiuae/falcon-7b-instruct"
falcon_llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.1, "max_new_tokens": 500}
)

# --------------------------------------------------------------
# Create the LLM chain and PromptTemplate
# --------------------------------------------------------------
template = """Question: {question}
Answer: You can think step by step.
"""

prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=falcon_llm)

# --------------------------------------------------------------
# Run the chain
# --------------------------------------------------------------

question = "How do I use the Large language models"
response = llm_chain.run(question)
wrapped_response = textwrap.fill(
    response, width=100, break_long_words=False, replace_whitespace=False
)
print(wrapped_response)

# --------------------------------------------------------------
# Load a video transcript from YouTube
# --------------------------------------------------------------

video_url = "https://www.youtube.com/watch?v=S5U76LPu_bQ&list=WL&index=3"
loader = YoutubeLoader.from_youtube_url(video_url)
transcript = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
docs = text_splitter.split_documents(transcript)

# --------------------------------------------------------------
# Summarize the transcript
# --------------------------------------------------------------

chain = load_summarize_chain(falcon_llm, chain_type="map_reduce", verbose=True)
print(chain.llm_chain.prompt.template)
print(chain.combine_document_chain.llm_chain.prompt.template)

# --------------------------------------------------------------
# Test the Falcon model
# --------------------------------------------------------------

output_summary = chain.run(docs)
wrapped_response = textwrap.fill(
    output_summary, width=100, break_long_words=False, replace_whitespace=False
)
print(wrapped_response)

# --------------------------------------------------------------
# Use OpenAI to compare
# --------------------------------------------------------------

openai_llm = OpenAI(model_name="text-davinci-003", temperature=0.1, max_tokens=500)
chain = load_summarize_chain(openai_llm, chain_type="map_reduce", verbose=True)
output_summary = chain.run(docs)
wrapped_response = textwrap.fill(
    output_summary, width=100, break_long_words=False, replace_whitespace=False
)
print(wrapped_response)
