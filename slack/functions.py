from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv(find_dotenv())


def draft_email(user_input, name="Ivan"):
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)

    template = """
    
    You are a helpful assistant that drafts an email reply based on an a new email.
    
    Your goal is to help the user quickly create a perfect email reply.
    
    Keep your reply short and to the point and mimic the style of the email so you reply in a similar manner to match the tone.
    
    Start your reply by saying: "Hi {name}, here's a draft for your reply:". And then proceed with the reply on a new line.
    
    Make sure to sign of with {signature}.
    
    """

    signature = f"Kind regards, \n\{name}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "Here's the email to reply to and consider any other comments from the user for reply as well: {user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(user_input=user_input, signature=signature, name=name)

    return response

def summarize_pdf(file):
    """
    Summarize a PDF file using the Hugging Face summarization pipeline.

    Args:
        file (str): The path to the PDF file to summarize.

    Returns:
        str: The summary of the PDF file.
    """
    # Import the pipeline
    from transformers import pipeline

    # Initialize the summarization pipeline
    summarizer = pipeline("summarization")

    # Read the PDF file
    with open(file, "rb") as f:
        pdf = f.read()

    # Convert the PDF to text
    text = pdf_to_text(pdf)

    # Summarize the text
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)

    return summary[0]["summary_text"]

    