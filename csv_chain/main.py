import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv


def main():
    load_dotenv(
        dotenv_path="/Users/ivanzhirnov/Downloads/ds_related/projects/langchain-experiments/.env"
    )

    st.set_page_config(
        page_title="Ask your CSV",
    )
    st.header("Ask your CSV")

    user_csv = st.file_uploader("Upload your CSV", type="csv")

    if user_csv is not None:
        user_question = st.text_input("Ask your question about your file: ")

        llm = OpenAI(temperature=0)
        agent = create_csv_agent(llm, user_csv, verbose=True)

        if user_question is not None and user_question != "":
            answer = agent.run(user_question)
            st.write(answer)


if __name__ == "__main__":
    main()
