import os
import json
import openai
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage, AIMessage, HumanMessage

# --------------------------------------------------------------
# OpenAI API
# --------------------------------------------------------------

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --------------------------------------------------------------
# Simple Question
# --------------------------------------------------------------

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {"role": "user", "content": "What is the weather in Karlstad, Sweden tomorrow?"}
    ],
)

output = completion.choices[0].message.content
print(output)

# --------------------------------------------------------------
# OpenAI Function Calling
# --------------------------------------------------------------

function_descriptions = [
    {
        "name": "get_weather_forecast",
        "description": "Get the weather forecast for a given city",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Name of the city, e.g. Stockholm",
                },
            },
            "required": ["location"],
        },
    }
]

user_prompt = "What is the weather in Karlstad, Sweden tomorrow?"

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": user_prompt}],
    # add function descriptions to the prompt
    functions=function_descriptions,
    function_call="auto",
)

output = completion.choices[0].message
print(output)

# --------------------------------------------------------------
# Create function
# --------------------------------------------------------------


def get_weather_forecast(location):
    """Get the weather forecast for a given city"""

    # Example output
    forecast_info = {
        "location": location,
        "datetime": str(datetime.now()),
        "temperature": "20°C",
        "wind_speed": "10m/s",
        "wind_direction": "East",
        "rain_probability": "0%",
        "sunrise": "06:00",
        "sunset": "18:00",
        "weather_description": "Clear sky",
    }

    return json.dumps(forecast_info)


# USe the LLM output to manually call the function
# The json.loads function converts the json string to a dictionary

location = json.loads(output.function_call.arguments).get("location")
params = json.loads(output.function_call.arguments)

# Call the function

chosen_function = eval(output.function_call.name)
forecast = chosen_function(**params)

print(forecast)

# --------------------------------------------------------------
# Add function result to the prompt for a final answer
# --------------------------------------------------------------

# The key is to add the function output back to the message
second_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {
            "role": "user",
            "content": user_prompt,
        },
        {
            "role": "function",
            "name": output.function_call.name,
            "content": forecast,
        },
    ],
    functions=function_descriptions,
)
response = second_completion.choices[0].message.content
print(response)
