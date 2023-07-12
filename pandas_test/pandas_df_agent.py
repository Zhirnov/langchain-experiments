from dotenv import find_dotenv, load_dotenv
from langchain import OpenAI
from langchain.agents import (
    load_tools,
    initialize_agent,
    create_pandas_dataframe_agent,
    Tool,
    AgentType,
)
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------------------
# Load API
# --------------------------------------------------------------

load_dotenv(find_dotenv())

# --------------------------------------------------------------
# Serp API tool
# --------------------------------------------------------------

llm = OpenAI(model_name="text-davinci-003", temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
agent.run(
    "what is the median salary of senior data scientist in 2023? What is the figure given there is a 10% increment?"
)

# --------------------------------------------------------------
# Load dataset
# --------------------------------------------------------------

df = pd.read_csv("../../langchain-experiments/pandas_test/ds_salaries.csv")

# --------------------------------------------------------------
# Initialize agent
# --------------------------------------------------------------

agent = create_pandas_dataframe_agent(llm, df, verbose=True)

# --------------------------------------------------------------
# Basic exploration
# --------------------------------------------------------------

agent.run("How many rows and columns are there in the dataset?")
agent.run("Are there any missing values in the dataset?")
agent.run("What are the columns?")
agent.run("How many categories are there in each column?")

# --------------------------------------------------------------
# Multiple steps
# --------------------------------------------------------------

agent.run("What is the median salary of senior data scientist in 2023?")
agent.run("What is company location has the most employees working remotely?")
agent.run(
    "Get median salaries of senior data scientist in each company size and plot in a bar chart"
)

# --------------------------------------------------------------
# Multiple dataframes
# --------------------------------------------------------------

df1 = df[df["work_year"] == 2022]
df2 = df[df["work_year"] == 2023]


agent = create_pandas_dataframe_agent(llm, [df1, df2], verbose=True)
