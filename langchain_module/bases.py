#! coding: utf-8

import unittest
import json
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from utils.tools import get_model_name, split_think_answer
from utils.ollama_utils import OllamaUtils
from langchain.schema import SystemMessage, HumanMessage


class TestLangChainOllama(unittest.TestCase):
    def setUp(self):
        self.model = get_model_name()

    def test_ollama_new_api(self):
        llm = Ollama(model=self.model, temperature=0.2)

        response, think = split_think_answer(llm.invoke("请使用中文介绍一下中国的四大发明。"))
        print(response)

    def test_ollama_utils(self):
        llm = OllamaUtils(model_name=self.model, temperature=0.2)

        response = llm.run("请使用中文介绍一下中国的四大发明。")
        print(response)

    def test_prompt_template(self):
        template_string = """
        Translate the text that is delimited by triple backticks into a style that is {style}.
        text: ```{text}```
        """

        prompt_template = ChatPromptTemplate.from_template(template_string)
        print('The first prompt in prompt template object:\n', prompt_template.messages[0].prompt)

        customer_style = """American English in a calm and respectful tone."""

        customer_email = """
        Arrr, I be fuming that me blender lid flew off and splattered me
        kitchen walls with smoothie! And to make matters worse, the warranty
        don't cover the cost of cleaning up me kitchen. I need yer help right
        now, matey!
        """

        customer_messages = prompt_template.format_messages(
            style=customer_style, text=customer_email)
        print(customer_messages[0])

        llm = OllamaUtils(model_name=self.model, temperature=0.2)

        response = llm.run(customer_messages[0].content)
        print(response)

    def test_reply_email(self):
        service_reply = """Hey there customer, \
        the warranty does not cover \
        cleaning expenses for your kitchen \
        because it's your falt that you misused your blender \
        by forgetting to put the lid on before starting the blender. \
        Tough luck! See ya!
        """

        service_style_pirate = """a polite tone that speaks in English Pirate."""

        service_messages = ChatPromptTemplate.from_template(
            """
            Translate the text that is delimited by triple backticks into a style that is {style}.
            text: ```{text}```
            """
        ).format_messages(
            style=service_style_pirate, text=service_reply
        )

        llm = OllamaUtils(model_name=self.model, temperature=0.2)
        service_response = llm.run(service_messages[0].content)
        print(service_response)

    def test_extract_review_info(self):
        customer_review = """\
        This leaf blower is pretty amazing. It has four settings:\
        candle blower, gentle breeze, windy city, and tornado. \
        It arrived in two days, just in time for my wife's \
        anniversary present. \
        I think my wife liked it so much she was speechless. \
        So far I've been the only one using it, and I've been \
        using it every other morning to clear the leaves on our lawn. \
        It's slightly more expensive than the other leaf blowers \
        out there, but I think it's worth it for the extra features.
        """

        review_template = """
        For the following text surrounded with triple backticks, extract the following information:
        
        gift: Was the item purchased as a gift for someone else? \
        Answer True if yes, False if not or unknown.
        
        delivery_days: How many days did it take for the product \
        to arrive? If this information is not found, output -1.
        
        price_value: Extract any sentences about the value or price, \
        and output them as a comma separated Python list.
        
        Format the output as JSON with the following keys:
        gift
        delivery_days
        price_value
        
        text: ```{text}```
        """

        review_prompt = ChatPromptTemplate.from_template(review_template)

        msgs = review_prompt.format_messages(
            text=customer_review
        )

        chat = OllamaUtils(model_name=self.model, temperature=0)
        response = chat.run(msgs[0].content)

        print("The result type: ", type(response))
        print("Result: ", response)

    def test_langchain_extractor(self):
        customer_review = """\
        This leaf blower is pretty amazing. It has four settings:\
        candle blower, gentle breeze, windy city, and tornado. \
        It arrived in two days, just in time for my wife's \
        anniversary present. \
        I think my wife liked it so much she was speechless. \
        So far I've been the only one using it, and I've been \
        using it every other morning to clear the leaves on our lawn. \
        It's slightly more expensive than the other leaf blowers \
        out there, but I think it's worth it for the extra features.
        """

        review_template = """
        For the following text surrounded with triple backticks, extract the following information:

        gift: Was the item purchased as a gift for someone else? \
        Answer True if yes, False if not or unknown.

        delivery_days: How many days did it take for the product \
        to arrive? If this information is not found, output -1.

        price_value: Extract any sentences about the value or price, \
        and output them as a comma separated Python list.

        Format the output as JSON with the following keys:
        gift
        delivery_days
        price_value

        text: ```{text}```
        """

        review_prompt = ChatPromptTemplate.from_template(review_template)

        gift_schema = ResponseSchema(
            name='gift',
            description="Was the item purchased as a gift for someone else? \
                        Answer True if yes, False if not or unknown.")

        delivery_days_schema = ResponseSchema(
            name='delivery_days',
            description="How many days did it take for the product to arrive? \
                        If this information is not found, output -1.")

        price_value_schema = ResponseSchema(
            name='price_value',
            description="Extract any sentences about the value or price, \
                        and output them as a comma separated Python list.")

        response_schemas = [
            gift_schema,
            delivery_days_schema,
            price_value_schema
        ]

        output_parser = StructuredOutputParser.from_response_schemas(
            response_schemas=response_schemas
        )

        format_instructions = output_parser.get_format_instructions()
        print(format_instructions)

        msgs = review_prompt.format_messages(
            text=customer_review, format_instructions=format_instructions)

        print("Prompt msg: ", msgs[0].content)

        chat = OllamaUtils(model_name=self.model, temperature=0)

        response = chat.run(msgs[0].content)
        print("The result: ", response)

        output_dict = output_parser.parse(response)
        print("The result type: ", type(output_dict))
        print("The result (after parsed): ", output_dict)

    def test_basic_1(self):
        llm = Ollama(model=self.model, temperature=0.0)

        res = llm.invoke("你是谁？")
        print(type(res))
        print(res)

    def test_basic_2_batch_mode(self):
        llm = Ollama(model=self.model, temperature=0.8)

        # 批量获取回答
        res = llm.generate(["请给我讲个笑话。", "请给我讲一个故事。",])
        print(type(res))
        print(res.llm_output)

        for data in res.generations:
            print(data)
            print(type(data[0]))
        print(res.dict())

    def test_chat_models_1(self):
        chat = ChatOllama(model=self.model, temperature=0.0)

        res = chat.invoke([
            SystemMessage(content="You are a writer."),
            HumanMessage(content="你是谁？"),
        ])
        print(res)
        print(type(res))

        res = chat.invoke([
            ('system', "You are a writer."),
            ('human', "你是谁？"),
        ])
        print(res)

    def test_model_create_api(self):
        client = Ollama()

        response = client.chat.completions.create(
            model=self.model,
            temperature=0.8,
            system="You are a helpful assistant.",
            prompt=["你是谁？", "你能给我什么帮助？"]
        )

        print(response.dict())
        print(response.choices[0].text)
        print(response.choices[1].text)
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
