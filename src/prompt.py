from random import randint

from openai import OpenAI
from dotenv import load_dotenv
import os

text = {
    "A": "Explore",
    "B": "Move randomly",
    "C": "Move towards a person",
    "D": "Move towards a door",
    "E": "Move towards window",
    "F": "Move towards the fire",
    "G": "Break window",
    "H": "Fight someone for a spot",
    "I": "Run through fire to safety",
    "J": "Jump out of building",
    "K": "Follow evacuation plan",
    "L": "Move to exit",
    "M": "Move to stair",
    "N": "Do nothing"
}

valid = text.keys()


def get_response(situation, options, temperature):
    context = ""
    with open("../data/context.txt", "r") as file:
        for line in file.readlines():
            context += line
            context += "\n"

    example = ""
    with open("../data/example.txt", "r") as file:
        for line in file.readlines():
            example += line
            example += "\n"
    question = "Options:\n" + options + "\n----------------------\nPick a letter:"

    with open("../data/openai_key.txt", "r") as file:
        OPENAI_API_KEY = file.readline().strip()
    if OPENAI_API_KEY is None:
        raise Exception("couldn't get key")
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    load_dotenv()
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",  # may change model
        temperature=temperature,  # will be passed in fear level
        max_tokens=3000,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": context},  # Will be prompt context
            {"role": "user", "content": situation},  # prompt of the user
            {"role": "assistant", "content": example},  # example of response
            {"role": "user", "content": question},  # form of question or command
        ]
    )
    return response


def get_random_choice(options):
    return options[randint(0, len(options) - 1)]


def get_choice_from_AI(situation, options, tempurature):
    options_with_text = ""
    for option in options:
        options_with_text += option
        options_with_text += ": "
        options_with_text += text[option]
        options_with_text += "\n"
    response = get_response(situation, options_with_text, tempurature)
    if response is None:
        return None
    if response == "" or response == " ":
        return None
    if response in valid:
        return response
    else:
        return None
