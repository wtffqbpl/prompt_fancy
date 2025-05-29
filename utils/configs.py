#! coding: utf-8

import os
import re
import openai
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv


# find_dotenv() loads environment variables from a .env file
# load_dotenv() loads the environment variables to the current environment


def get_openai_client():
    _ = load_dotenv(find_dotenv())

    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_openrouter_client():
    _ = load_dotenv(find_dotenv())
    openrouter_key = os.environ["OPENROUTER_API_KEY"]
    base_url = "https://openrouter.ai/api/v1"

    return OpenAI(api_key=openrouter_key, base_url=base_url)


def get_llm_client(model='gpt-3.5-turbo'):
    """ Configure OpenAI API key and base URL."""
    if re.match(".*qwen.*", model):
        return get_openrouter_client()
    else:
        return get_openai_client()


def get_model_name():
    """ Get the model name from the environment variable."""
    _ = load_dotenv(find_dotenv())
    model_name = os.environ["MODEL_NAME"]
    return model_name


def get_open_weather_api_key():
    _ = load_dotenv(find_dotenv())
    open_weather_api_key = os.environ["OPEN_WEATHER_API_KEY"]
    return open_weather_api_key


if __name__ == "__main__":
    pass
