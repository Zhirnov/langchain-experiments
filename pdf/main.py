from dotenv import load_dotenv
import os
from langchain.memory import ConversationBufferMemory, ConversationEntityMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.chains import ConversationChain
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE


def main():
    load_dotenv()

    # test api key
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set. Please add it to your .env file.")
        exit(1)
    else:
        print("OPENAI_API_KEY is set.")

    # Old method
    # chat = ChatOpenAI(temperature=0.9)

    # messages = [
    #     SystemMessage(content="You are a helpful chatbot."),
    # ]

    # print("Welcome to the chatbot.")

    # while True:
    #     user_input = input("> ")

    #     messages.append(HumanMessage(content=user_input))

    #     ai_response = chat(messages)

    #     print("\nAssisntant:\n", ai_response.content)

    #     messages.append(AIMessage(content=ai_response.content))

    # Buffer memory
    # llm = ChatOpenAI()
    # conversation = ConversationChain(
    #     llm=llm, memory=ConversationBufferMemory(), verbose=True
    # )
    # print("Welcome to the chatbot.")

    # while True:
    #     user_input = input("> ")
    #     ai_response = conversation.predict(input=user_input)

    #     print("\nAssisntant:\n", ai_response)

    # Entity memory
    llm = ChatOpenAI()
    conversation = ConversationChain(
        llm=llm,
        memory=ConversationEntityMemory(llm=llm),
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        verbose=True,
    )
    print("Welcome to the chatbot.")

    while True:
        user_input = input("> ")
        ai_response = conversation.predict(input=user_input)

        print("\nAssisntant:\n", ai_response)


if __name__ == "__main__":
    main()
