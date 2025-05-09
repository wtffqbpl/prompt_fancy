#! coding: utf-8

import unittest
from utils.tools import get_model_name, get_completion


class TestIterativePromptDevelopment(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()

        self.lamp_review = """
        Needed a nice lamp for my bedroom, and this one had \
        additional storage and not too high of a price point. \
        Got it fast. The string to our lamp broke during the \
        transit and the company happily sent over a new one. \
        Came within a few days as well. It was easy to put \
        together. Then I had a missing part, so I contacted their \
        support and they very quickly got me the missing piece! \
        Lumina seems to me to be a great company that cares \
        about their customers and products!!
        """

        self.story = """
        In a recent survey conducted by the government,
        public sector employees were asked to rate their level
        of satisfaction with the department they work at.
        The results revealed that NASA was the most popular
        department with a satisfaction rating of 95 %.
        
        One NASA employee, John Smith, commented on the findings,
        stating, "I'm not surprised that NASA came out on top.
        It's a great place to work with amazing people and
        incredible opportunities. I'm proud to be a part of
        such an innovative organization."
        
        The results were also welcomed by NASA's management team,
        with Director Tom Johnson stating, "We are thrilled to
        hear that our employees are satisfied with their work at NASA.
        We have a talented and dedicated team who work tirelessly
        to achieve our goals, and it's fantastic to see that their
        hard work is paying off."
        
        The survey also revealed that the
        Social Security Administration had the lowest satisfaction
        rating, with only 45% of employees indicating they were
        satisfied with their job. The government has pledged to
        address the concerns raised by employees in the survey and
        work towards improving job satisfaction across all departments.
        """

    def test_summarization_1(self):

        prompt = f"""
        What is the sentiment of the following product review, which is
        delimited with triple backticks?
        
        Review text: ```{self.lamp_review}```
        """

        result, think = get_completion(prompt, model=self.model)
        print(result)

    def test_summarization_2(self):

        prompt = f"""
        What is the sentiment of the following product review, which is
        delimited with triple backticks?
        
        Give your answer as a single word, either "positive" or "negative".
        
        Review text: ```{self.lamp_review}```
        """

        result, think = get_completion(prompt, model=self.model)
        print(result)

    def test_summarization_3(self):
        # 识别情感类型

        prompt = f"""
        Indentify a list of emotions that the writer of the \
        following review is expressing. Include no more than \
        five items in the list. Format your answer as a list of \
        lower-case words separated by commas.
        
        Review text: ```{self.lamp_review}```
        """

        result, think = get_completion(prompt, model=self.model)
        print(result)

    def test_summarization_4(self):
        # 识别愤怒

        prompt = f"""
        Is the writer of the following review expressing anger? \
        The review is delimited with triple backticks. \
        Give your answer as either yes or no.
        
        Review text: ```{self.lamp_review}```
        """

        result, think = get_completion(prompt, model=self.model)
        print(result)

    def test_summarization_5(self):
        # 商品信息提取
        # 信息提取时自然语言处理(NLP) 的重要组成部分，它帮助我们从文本中抽取
        # 特定的、我们关心的信息。

        prompt = f"""
        Indentify the following items from the review text:
        - Item purchased by reviewer
        - Company that made the item
        
        The review is delimited with triple backticks. \
        Format your response as a JSON object with \
        "Item" and "Brand" as the keys.
        If the information isn't present, use "unknown" \
        as the value.
        Make your response as short as possible
        
        Review text: ```{self.lamp_review}```
        """

        result, think = get_completion(prompt, model=self.model)
        print(result)

    def test_summarization_6(self):
        # 商品信息提取
        # 事实上，我们可以设计一个单一的Prompt，来同时提取所有这些信息。

        prompt = f"""
        Indentify the following items from the review text:
        - Sentiment (positive or negative)
        - is the reviewer expressing anger? (true or false)
        - Item purchased by reviewer
        - Company that made the item
        
        The review is delimited with triple backticks. \
        Format your response as a JSON object with \
        "Sentiment", "Anger", "Item" and "Brand" as the keys.
        If the information isn't present, use "unknown" \
        as the value.
        Make your response as short as possible.
        Format the Anger value as a boolean.
        
        Review text: ```{self.lamp_review}```
        """

        result, think = get_completion(prompt, model=self.model)
        print(result)

    def test_summarization_7(self):
        # 推断讨论主题
        # 大语言模型的另外一个很酷的应用就是推断主题。假设我们有一段长文本，我们如何
        # 判断这段文本的主旨式神？它涉及了哪些主题。

        prompt = f"""
        Determine five topics that are being discussed in the \
        following text, which is delimited by triple backticks.
        
        Make each item one or two words long.
        
        Format your response as a list of items separated by commas.
        Give me a list which can be read in Python.
        
        ONLY OUTPUT THE FINAL LIST, DO NOT INCLUDE ANY OTHER TEXT.
        
        Text sample: ```{self.story}```
        """

        result, think = get_completion(prompt, model=self.model)
        print(result.split(sep=','))

    def test_summarization_8(self):
        # 推断讨论主题
        # 大语言模型的另外一个很酷的应用就是推断主题。假设我们有一段长文本，我们如何
        # 判断这段文本的主旨式神？它涉及了哪些主题。

        topic_list = [
            'nasa',
            'local government',
            'engineering',
            'employee satisfaction',
            'federal government',
        ]

        prompt = f"""
        Determine whether each item in the following list of \
        topics is a topic in the text below, which is delimited with \
        triple backticks.
        
        Give your answer as list with 0 or 1 for each topic.
        
        List of topics: {', '.join(topic_list)}
        
        ONLY OUTPUT THE FINAL LIST, DO NOT INCLUDE ANY OTHER TEXT.
        
        Text sample: ```{self.story}```
        """

        result, think = get_completion(prompt, model=self.model, temperature=0.2)
        print(result)

        topic_dict = {topic_list[i] : eval(result)[i] for i in
                      range(len(eval(result)))}
        print(topic_dict)
        if topic_dict['nasa'] == 1:
            print("NASA is mentioned in the text.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
