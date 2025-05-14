#! coding: utf-8

import os
from dotenv import load_dotenv


load_dotenv()

# model configurations
PLATFORM = os.getenv("PLATFORM", "ollama")
MODEL = os.getenv("MODEL", "llama3.2")

# database configurations
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:password@localhost:5432/chatbot")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
