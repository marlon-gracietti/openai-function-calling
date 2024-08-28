import os
import openai
import json
from dotenv import load_dotenv, find_dotenv

# Load the .env file
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

print("Hello! How can I help you today?")

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="celsius"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "24",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info, indent=2)

# Define the function specification for OpenAI
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

# User's message
messages = [
    {
        "role": "user",
        "content": "What's the weather like in Balneário Camboriú?"
    }
]

try:
    # ChatCompletion request
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto"  # Enable the function call feature
    )

    # Extracting the response
    response_message = response.choices[0].message

    if 'function_call' in response_message:
        function_name = response_message['function_call']['name']
        function_args = json.loads(response_message['function_call']['arguments'])

        if function_name == "get_current_weather":
            weather_response = get_current_weather(
                location=function_args.get("location"),
                unit=function_args.get("unit", "celsius")
            )
            print("Weather response:", weather_response)
    else:
        print("Response:", response_message['content'])

except Exception as e:
    print("An error occurred:", str(e))
