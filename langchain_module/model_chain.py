#! coding: utf-8

import unittest
import warnings
from itertools import product
import pandas as pd
from pprint import pprint

from langchain.chains.sequential import SimpleSequentialChain
from langchain.chains import SequentialChain

warnings.filterwarnings("ignore")

from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from utils.tools import get_model_name, split_think_answer


class TestLangChainMemoryModule(unittest.TestCase):
    def setUp(self):
        self.model_name = get_model_name()
        self.llm = ChatOllama(model=self.model_name, temperature=0.0)

    def test_model_chain_1(self):
        prompt = ChatPromptTemplate.from_template("描述制造{product}的一个公司的最佳名称是什么？")

        chain = LLMChain(llm=self.llm, prompt=prompt,)

        product = "大号床单套装"
        response, think = split_think_answer(chain.run(product))
        print(response)

    def test_sequential_chain(self):
        # The first prompt
        first_prompt = ChatPromptTemplate.from_template(
            "描述制造{product}的一个公司最佳名称是什么？直接给出公司名称，不要解释，同时要求公司名称为中文名。")
        chain = LLMChain(llm=self.llm, prompt=first_prompt,)

        # The second prompt
        second_prompt = ChatPromptTemplate.from_template(
            "对于下面这个公司写一个20字的 {company_name}。")
        chain_two = LLMChain(llm=self.llm, prompt=second_prompt)

        overall_simple_chain = SimpleSequentialChain(chains=[chain, chain_two], verbose=True)

        product = "大号床单套装"
        response, think = split_think_answer(overall_simple_chain.run(product))
        print(response)

    def test_sequential_chain_2(self):
        llm = ChatOllama(model=self.model_name, temperature=0.9)

        ######### Chain 1
        first_prompt = ChatPromptTemplate.from_template(
            "把下面的中文翻译成英文:"
            "\n\n{text}."
        )
        # chain 1: input: Review, output: English_Review
        translate_en_chain = LLMChain(
            llm=llm, prompt=first_prompt, output_key="translated_text")

        ######### Chain 2
        second_prompt = ChatPromptTemplate.from_template(
            "将以下英文文本格式化为更正式的语气:"
            "\n\n{translated_text}"
        )
        # chain 2: input: translated_text, output: formatted_text
        format_chain = LLMChain(
            llm=llm, prompt=second_prompt, output_key="formatted_text")

        ######## Chain 3
        third_prompt = ChatPromptTemplate.from_template(
            "请为一下英文文本生成一个简短摘要:\n\n{formatted_text}"
        )
        # input: Review, output: Language
        summarize_chain = LLMChain(
            llm=llm, prompt=third_prompt, output_key="summary")

        ######## Chain 4
        forth_prompt = ChatPromptTemplate.from_template(
            "将以下英文文本翻译回中文:\n\n{summary}"
        )
        # input: summary, language, output: followup_message
        translate_zh_chain = LLMChain(
            llm=llm, prompt=forth_prompt, output_key="back_translated_text")

        overall_chain = SequentialChain(
            chains=[translate_en_chain, format_chain, summarize_chain, translate_zh_chain],
            input_variables=["text"],
            output_variables=["translated_text", "formatted_text", "summary", "back_translated_text"],
            verbose=True
        )

        input_text = "这个产品太棒了！用户体验非常好。"
        response = overall_chain.apply({"text": input_text})
        pprint(response)




if __name__ == '__main__':
    unittest.main(verbosity=2)
