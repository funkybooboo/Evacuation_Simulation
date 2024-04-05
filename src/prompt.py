from openai import OpenAI
from dotenv import load_dotenv
import os


def get_response(context):
    OPENAI_API_KEY = None
    with open("APIKEY.txt", "r") as file:
        OPENAI_API_KEY = file.readline().strip()
    if OPENAI_API_KEY is None:
        raise Exception("couldnt get key")
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    load_dotenv()
    client = OpenAI()

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo-0125", # may change model
        temperature = 0.8, # will be passed in fear level
        max_tokens = 3000,
        response_format={"type": "json_object"},
        messages = [
            {"role": "system", "content": ""}, # Will be prompt context 
            {"role": "user", "content": ""}, # prompt of the user
            {"role": "assistant", "content": ""}, # example of response
            {"role": "user", "content": ""}, # form of question or command
        ]
    )
    return response
