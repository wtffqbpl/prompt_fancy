#! coding: utf-8

from langchain_ollama import OllamaLLM
from utils.tools import split_think_answer


class OllamaUtils:
    def __init__(self, model_name: str, temperature: float = 0.2) -> None:
        self.model_name = model_name
        self.temperature = temperature
        self.llm = OllamaLLM(model=self.model_name, temperature=self.temperature)

    def run(self, prompt: str) -> str:
        response, think = split_think_answer(self.llm.invoke(prompt))
        return response
