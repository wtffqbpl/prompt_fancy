#! coding: utf-8

import unittest
from langchain.chains import ConversationChain
from langchain_ollama.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory import ConversationTokenBufferMemory
from langchain.memory import ConversationSummaryBufferMemory
from utils.tools import get_model_name, split_think_answer


class TestLangChainMemoryModule(unittest.TestCase):

    def setUp(self):
        self.model = get_model_name()
        self.llm = ChatOllama(model=self.model, temperature=0.2)

    def test_conversation_memory_basic(self):
        # Define memory
        memory = ConversationBufferMemory()

        # Define chain
        # verbose设置为True时，程序会输出更详细的信息，以提供更多的调试或运行信息。
        # 相反，verbose设置为False时，程序会以更简洁的形式运行，只输出关键的信息。
        conversation = ConversationChain(llm=self.llm, memory=memory, verbose=True)

        # Run the chain with a user input
        response, think = split_think_answer(conversation.run("你好，我叫皮皮鲁。"))
        print(response)

        # The second round conversation
        response, think = split_think_answer(conversation.run("1+1等于多少？"))
        print(response)

        # The third round conversation
        response, think = split_think_answer(conversation.run("你知道我的名字吗？"))
        print(response)

        # 查看储存缓存(buffer), 即c㽾了当前为止所有的对话信息。
        print(memory.buffer)

        # 也可以通过load_memory_variables()方法来加载缓存。
        print(memory.load_memory_variables({}))

    def test_add_dialogue_manually(self):
        # LLM本身是无状态的，语言模型本身并不记得到目前为止的历史对话。Memory 可以储存到目前为止所有的的术语
        # 或对话，并将其输入或附加上下文到LLM中用于生成输出。
        memory = ConversationBufferMemory()
        memory.save_context({"input": "你好，我叫皮皮鲁。"}, {"output": "你好啊，我叫路路西。"})
        res = memory.load_memory_variables({})

        print(res)

        memory.save_context({'input': "很高兴和你成为朋友！"},
                            {'output': "是的，让我们一起去冒险吧！"})

        res = memory.load_memory_variables({})
        print(res)

    def test_conversation_window_memory(self):
        # Define chain. k=1 means only the last round of conversation is kept in memory.
        memory = ConversationBufferWindowMemory(k=1)

        memory.save_context({"input": "你好，我叫皮皮鲁。"},
                           {"output": "你好啊，我叫路路西。"})
        memory.save_context({'input': "很高兴和你成为朋友！"},
                           {"output": "是的，让我们一起去冒险吧！"})

        res = memory.load_memory_variables({})
        print(res)

    def test_conversation_window_memory_2(self):
        memory = ConversationBufferWindowMemory(k=1)
        conversation = ConversationChain(llm=self.llm, memory=memory, verbose=True)

        print("The first round conversation:")
        response, think = split_think_answer(conversation.run("你好，我叫皮皮鲁。"))
        print(response)

        print("The second round conversation:")
        response, think = split_think_answer(conversation.run("1+1等于多少？"))
        print(response)

        print("The third round conversation.")
        response, think = split_think_answer(conversation.run("你知道我的名字吗？"))
        print(response)

    def test_conversation_token_memory(self):
        memory = ConversationTokenBufferMemory(llm=self.llm, max_token_limit=30)
        memory.save_context({"input": "朝辞白帝彩云间，"}, {"output": "千里江陵一日还。"})
        memory.save_context({"input": "两岸猿声啼不住，"}, {"output": "轻舟已过万重山。"})
        res = memory.load_memory_variables({})

        print(res)

    def test_conversation_summary_memory(self):
        # create a long string
        schedule = """
        在八点你和你的产品团队有一个会议。 \
        你需要做一个PPT。 \
        上午9点到12点你需要忙于LangChain。\
        Langchain是一个有用的工具，因此你的项目进展的非常快。\
        中午，在意大利餐厅与一位开车来的顾客共进午餐 \
        走了一个多小时的路程与你见面，只为了解最新的 AI。 \
        确保你带了笔记本电脑可以展示最新的 LLM 样例.
        """
        memory = ConversationSummaryBufferMemory(llm=self.llm, max_token_limit=32 * 1024)
        memory.save_context({'input': "你好，我是皮皮鲁。"},
                           {"output": "你好啊，我叫鲁西西。"})
        memory.save_context({"input": "很高兴和你成为朋友。"},
                            {"output": "是的，让我们一起去冒险吧！"})

        memory.save_context({"input": "今天的日程安排是什么？"},
                            {"output": f"{schedule}"})

        print(memory.load_memory_variables({})['history'])

        conversation = ConversationChain(llm=self.llm, memory=memory, verbose=True)
        response, think = split_think_answer(conversation.run(input="展示什么样的样例最好呢？"))
        print(response)

        res = memory.load_memory_variables({})
        print(res)


if __name__ == '__main__':
    unittest.main(verbosity=2)
