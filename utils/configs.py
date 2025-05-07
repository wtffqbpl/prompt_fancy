#! coding: utf-8

import os
import openai
from dotenv import load_dotenv, find_dotenv


# find_dotenv() loads environment variables from a .env file
# load_dotenv() loads the environment variables to the current environment


def get_openai_key():
    _ = load_dotenv(find_dotenv())
    return os.environ["OPENAI_API_KEY"]


# Set OpenAI API key
openai.api_key = get_openai_key()


if __name__ == "__main__":
    print("OpenAI API Key: ", get_openai_key())
    print(openai.api_key)
    pass
