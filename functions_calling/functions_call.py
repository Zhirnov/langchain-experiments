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
# Example from OpenAI Documentation
# --------------------------------------------------------------


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "What's the weather like in Boston?"}]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response


print(run_conversation())


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
