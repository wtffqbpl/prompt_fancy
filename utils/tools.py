#! coding: utf-8


import os
import re
import requests
from dotenv import load_dotenv, find_dotenv
from typing import Optional, Tuple
from utils.configs import get_llm_client
from utils.configs import get_model_name
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import urllib.parse


def show_html_content(html_content=None):
    # ChromeDriver configuration
    service = Service(executable_path='/opt/homebrew/bin/chromedriver')
    opts = Options()

    driver = webdriver.Chrome(service=service, options=opts)

    data_url = "data:text/html;charset=utf-8," + urllib.parse.quote(html_content)
    driver.get(data_url)

    # Wait for the page to load
    input("Press Enter to close the browser...")

    driver.quit()
    pass


def split_think_answer(text: str) -> Tuple[Optional[str], str]:
    """
    将 text 中的 <think>...</think> 部分提取为 think_content，
    并将剩余内容作为 answer_content 返回。

    :param text: 包含 <think> 标签和回答的原始字符串
    :return: (think_content, answer_content)
             think_content 如果没有标签则为 None
             answer_content 去掉 <think> 标签部分后的回答文本
    """
    # 匹配 <think> 标签及其中内容（支持跨行）
    pattern = re.compile(r'<think>(.*?)</think>', re.DOTALL)
    match = pattern.search(text)

    if match:
        think_content = match.group(1).strip()
        # 去掉整个 <think>…</think> 片段，剩下的即为回答内容
        answer_content = pattern.sub('', text).strip()
    else:
        think_content = None
        answer_content = text.strip()

    return answer_content, think_content


class OpenAIClient:

    @staticmethod
    def get_completion(prompt, sys_prompt=None, model='gpt-3.5-turbo', temperature=0.0):
        """ Get completion from OpenAI API using the given prompt and model."""

        # Configure OpenAI API key and base URL
        client = get_llm_client(model)

        messages = [
            {'role': 'user', 'content': prompt}
        ]

        # Add system prompt if provided
        if sys_prompt:
            messages.insert(0, {'role': 'system', 'content': sys_prompt})

        response = client.chat.completions.create(
            model=model, messages=messages, temperature=temperature)

        # return the content of the response
        return response.choices[0].message.content

    @staticmethod
    def get_completion_from_messages(messages, model='gpt-3.5-turbo', temperature=0.0, max_tokens=32*1024):
        client = get_llm_client(model)
        response = client.chat.completions.create(
            model=model, messages=messages, temperature=temperature, max_tokens=max_tokens)
        return response.choices[0].message.content


class OllamaClient:

    @staticmethod
    def get_completion(user_prompt, model='llama3.2', sys_prompt=None, temperature=0.0):
        messages = [
            {'role': 'user', 'content': user_prompt}
        ]

        if sys_prompt:
            messages.insert(0, {'role': 'system', 'content': sys_prompt})

        payload = {
            'model': model,
            'messages': messages,
            'temperature': temperature
        }

        url = 'http://localhost:11434/v1/chat/completions'
        response = requests.post(url, json=payload)
        data = response.json()
        return data['choices'][0]['message']['content']

    @staticmethod
    def get_completion_from_messages(messages, model='llama3.2', temperature=0.0, max_tokens=32*1024):
        payload = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
        }

        url = 'http://localhost:11434/v1/chat/completions'
        response = requests.post(url, json=payload)
        data = response.json()
        return data['choices'][0]['message']['content']


def get_completion(user_prompt, model='llama3.2', sys_prompt=None, temperature=0.0):
    """ Get completion from OpenAI API using the given prompt and model."""
    _ = load_dotenv(find_dotenv())
    platform = os.environ["PLATFORM"]

    if platform == 'ollama':
        msg = OllamaClient.get_completion(
            user_prompt, model=model, sys_prompt=sys_prompt, temperature=temperature)
    else:
        msg = OpenAIClient.get_completion(
            user_prompt, sys_prompt=sys_prompt, model=model, temperature=temperature)

    return split_think_answer(msg)


def get_completion_from_messages(messages, model='qwen3:1.7b', temperature=0.0, max_tokens=32*1024):

    _ = load_dotenv(find_dotenv())
    platform = os.environ["PLATFORM"]
    if platform == 'ollama':
        msg = OllamaClient.get_completion_from_messages(
            messages, model=model, temperature=temperature)
    else:
        msg = OpenAIClient.get_completion_from_messages(
            messages, model=model, temperature=temperature)
    return split_think_answer(msg)


if __name__ == '__main__':
    sys_prompt = '你是一个专业的星座分析师。'
    user_prompt = '请简要分析双子座的性格特征和运势特点。'
    # get_completion(sys_prompt, user_prompt, model="qwen/qwen3-235b-a22b:free", temperature=0.7)

    model = get_model_name()
    answer_content, think_content = get_completion(sys_prompt, model=model, temperature=0.7)
    print("THINK:", think_content)
    print("ANSWER:", answer_content)
