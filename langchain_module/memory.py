#! coding: utf-8

# 当使用Langchain中的Memory 模块时，它旨在保存、组织和跟踪整个对话历史，从而为用户
# 和模型之间的交互提供连续的Context。
# LangChain 提供了多种存储类型。其中:
#   **缓冲区存储** 允许保留最近的聊天消息，
#   **摘要存储** 则提供了对整个对话的摘要。
#   **实体存储** 则允许在多轮对话中保留有关特定实体的信息。
# 这些记忆组件都是模块化的，可与其他组件组合使用，从而增强机器人的对话管理能力。
# 存储模块可以通过简单的API调用来访问和更新，允许开发人员轻松实现对话历史记录
# 的管理和维护。
# 主要包含四种存储模块，其他模块可以查看文档
#  * 对话缓存储存 (ConversationBufferMemory)
#  * 对话缓存窗口存储 (ConversationBufferWindowMemory)
#  * 对话令牌缓存储存 (ConversationTokenBufferMemory)
#  * 对话摘要存储 (ConversationSummaryBufferMemory)

import unittest
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List

from tenacity.stop import stop_base

from utils.tools import get_model_name


# Implement a simple message history
class InMemoryHistory(BaseChatMessageHistory):
    def __init__(self):
        self.messages = []

    def add_message(self, message: BaseMessage) -> None:
        self.messages.append(message)

    def clear(self) -> None:
        self.messages = []


class TestLangChainMemoryModule(unittest.TestCase):
    def setUp(self):
        self.model = get_model_name()
        self.llm = OllamaLLM(model=self.model, temperature=0.0)
        self.store = {}

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = InMemoryHistory()
        return self.store[session_id]

    def test_conversation_memory_basic(self):
        # Define prompt
        prompt = PromptTemplate.from_template(
            "You are a helpful AI assistant.\n\n"
            "History: {history}\n"
            "User: {input}\n"
            "Assistant:")

        # Define chain
        chain = prompt | self.llm

        # Create runnable with message history
        runnable = RunnableWithMessageHistory(
            chain,
            self.get_session_history,
            input_messages_key="input",
            history_factory_key="history")

        # Conversation configs
        config: RunnableConfig = {'configurable': {'session_id': 'abc123'}}

        # First message
        response = runnable.invoke(
            input={'input': '你好，我是皮皮鲁。', 'history': ""},
            config=config)
        print(response)

        # Second message
        response = runnable.invoke(
            input={'input': '1+1等于多少。', 'history': ''},
            config=config)
        print(response)


if __name__ == '__main__':
    unittest.main(verbosity=2)
