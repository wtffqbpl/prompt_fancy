#! coding: utf-8

import unittest
from utils.tools import get_model_name, get_completion, get_completion_from_messages


class TestLLMTokenCount(unittest.TestCase):
    def setUp(self):
        self.model = get_model_name()

    def test_word_tokens(self):
        prompt = "Take the letters in lollipop and reverse them"

        response, think = get_completion(prompt, model=self.model)

        print(response)

    def test_word_tokens_1(self):
        prompt = """
        Take the letters in l-o-l-l-i-p-o-p and reverse them
        
        ONLY OUTPUT THE REVERSED LETTERS, DO NOT OUTPUT ANY OTHER TEXT.
        """

        response, think = get_completion(prompt, model=self.model)

        print(response)

    def test_word_tokens_2(self):
        prompt = """
        What is the capital of France, and the attitude and latitude of this city?
        
        ONLY OUTPUT THE CITY NAME AND THE ATTITUDE AND THE LATITUDE WITH JSON FORMAT, \
        DO NOT OUTPUT ANY OTHER TEXT.
        """
        response, think = get_completion(prompt, model=self.model)
        print(response)

    def test_3(self):
        msgs = [
            {'role': 'system', 'content': 'You are an assistant who responds in the style of Dr Seuss.'},
            {'role': 'user', 'content': 'write me a very short poem about carrot.'},
        ]

        response, think = get_completion_from_messages(messages=msgs, model=self.model)

        print(response)

        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
