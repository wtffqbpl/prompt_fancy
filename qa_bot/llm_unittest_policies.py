#! coding: utf-8

import unittest
import os
import json
from pprint import pprint

from sqlalchemy import custom_op

from utils.tools import get_model_name, get_completion_from_messages
from qa_bot.qa_bot_utils import (
    create_products,
    get_products_and_category,
    get_products_from_query,
    read_string_to_list,
    get_mentioned_product_info,
    answer_user_msg
)


def find_category_and_product_v1(user_input, products_and_category, model):
    """
    Find the category and product from the user input.
    """
    delimiter = '####'

    # system message which is used to guide the model generation
    system_msg = f"""
    You will be provided with customer service queries. \
    the customer service query will be delimited with {delimiter} characters.
    
    Output a Python list of json objects, where each object has the following format: \
        'category': <one of Computers and Laptops, Smartphones and Accessories, Televisions and Home Theater Systems, \
                    Gaming Consoles and Accessories, Audio Equipment, Cameras and Camcorders>,
        AND
        'products': <a list of ALL products found in the allowed product list below>
        
    Where the categories and products must be found in the customer service query.
    If a product is mentioned, it must be associated with the correct category in the allowed product list below.
    If no products or categories are found, output an empty list.

    List out all products that are relevant to the customer service query based on how closely it relates \
    to the product name and product category.
    Do not assume, from the name of the product, any features or attributes such as relative quality or price.
    
    The allowed products are provided in JSON format.
    The keys of each item represent the category.
    The values of each item is a list of products that are within that category.
    
    Allowed products: {products_and_category}
    """

    # Provide few examples to the model
    few_shot_user_1 = """I want the most expensive computer."""
    few_shot_assistant_1 = """
    [
        {
            "category": "Computers and Laptops",
            "products": [
                "TechPro Ultrabook",
                "BlueWave Gaming Laptop",
                "PowerLite Convertible",
                "TechPro Desktop",
                "BlueWave Chromebook"
            ]
        }
    ]"""

    msgs = [
        {'role': 'system', 'content': system_msg},
        {'role': 'user', 'content': f"{delimiter}{few_shot_user_1}{delimiter}"},
        {'role': 'assistant', 'content': f"{delimiter}{few_shot_assistant_1}{delimiter}"},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"}
    ]

    response, think = get_completion_from_messages(msgs, model)

    return response


class TestQA(unittest.TestCase):
    def setUp(self):
        self.model = get_model_name()
        self.all_messages = []
        if not os.path.exists('products.json'):
            create_products()
        self.products_and_category = get_products_and_category()

    def test_process_user_message(self):

        customer_msg_0 = f"""Which TV can I buy if I'm on a budget?"""
        products_by_category_0 = find_category_and_product_v1(
            customer_msg_0, self.products_and_category, model=self.model)
        pprint(json.loads(products_by_category_0.replace('\'', '\"')))

        customer_msg_1 = f"""I need a charger for my smartphone."""
        products_by_category_1 = find_category_and_product_v1(
            customer_msg_1, self.products_and_category, model=self.model)
        pprint(json.loads(products_by_category_1.replace('\'', '\"')))

        customer_msg_2 = f"""I want to buy a new camera."""
        products_by_category_2 = find_category_and_product_v1(
            customer_msg_2, self.products_and_category, model=self.model)
        pprint(json.loads(products_by_category_2.replace('\'', '\"')))

        customer_msg_3 = f"""I need a new laptop for gaming."""
        products_by_category_3 = find_category_and_product_v1(
            customer_msg_3, self.products_and_category, model=self.model)
        pprint(json.loads(products_by_category_3.replace('\'', '\"')))

        customer_msg_4 = f"""I want to buy a new smartphone."""
        products_by_category_4 = find_category_and_product_v1(
            customer_msg_4, self.products_and_category, model=self.model)
        pprint(json.loads(products_by_category_4.replace('\'', '\"')))

    def test_test_5(self):
        customer_msg_5 = f"""tell me about the smartx pro phone and the fotosnap camera, the dslr one.
        Also, what TVs do you have?"""
        products_by_category_5 = find_category_and_product_v1(
            customer_msg_5, self.products_and_category, model=self.model)
        pprint(json.loads(products_by_category_5.replace('\'', '\"')))

    def test_test_6(self):
        customer_msg = f"""如果我预算有限，我可以买哪款电视?"""
        products_by_category = find_category_and_product_v1(
            customer_msg, self.products_and_category, model=self.model)
        pprint(json.loads(products_by_category.replace('\'', '\"')))

    def test_test_7(self):
        customer_msg = f"""你们有哪些电脑？"""
        products_by_category = find_category_and_product_v1(
            customer_msg, self.products_and_category, model=self.model)
        pprint(json.loads(products_by_category.replace('\'', '\"')))

    def test_test_8(self):
        customer_msg = f"""告诉我关于CineView电视的信息，那款8K的，还有Gameshpere游戏机，X款的。
        我预算有限，你们有哪些电脑？"""
        products_by_category = find_category_and_product_v1(
            customer_msg, self.products_and_category, model=self.model)
        pprint(json.loads(products_by_category.replace('\'', '\"')))


def find_category_and_product_v2(user_input, products_and_category, model):
    delimiter = "####"

    system_msg = f"""
    You will be provided with customer service queries. \
    The customer service query will be delimited with {delimiter} characters.
    Output a Python list of JSON objects, where each object has the following format:
        'category': <one of Computers and Laptops, Smartphones and Accessories, Televisions and Home Theater Systems, \
                    Gaming Consoles and Accessories, Audio Equipment, Cameras and Camcorders>,
    AND
        'products': <a list of ALL products found in the allowed product list below>
    
    Do not output any additional text that is not in JSON format.
    Do not write any explanatory text after outputting the requested JSON.
    
    where the categories and products must be found in the customer service query.
    
    if a product is mentioned, it must be associated with the correct category in the allowed product list below.
    If no products or categories are found, output an empty list.
    
    List out all products that are relevant to the customer service query based on how closely it relates \
    to the product name and product category.
    
    Do not assume, from the name of the product, any features or attributes such as relative quality or price.
    
    The allowed products are provided in JSON format.
    The keys of each item represent the category.
    The values of each item is a list of products that are within that category.
    Allowed products: {products_and_category}
    
    BEFORE OUTPUT THE FINAL RESULTS, PLEASE CHECK THE OUTPUT JSON FORMAT, IF IT IS NOT IN CORRECT JSON FORMAT, \
    PLEASE FIX IT BEFORE OUTPUT THE FINAL RESULTS.
    """

    few_shot_user_1 = """I want the most expensive computer. What do you recommend?"""
    few_shot_assistant_1 = """
    [
        {'category': 'Computers and Laptops', \
         'products': ['TechPro Ultrabook', 'BlueWave Gaming Laptop', \
                      'PowerLite Convertible', 'TechPro Desktop', 'BlueWave Chromebook']
        }
    ]
    """

    few_shot_user_2 = """I want the most cheapest computer. What do you recommend?"""
    few_shot_assistant_2 = """
    [
        {'category': 'Computers and Laptops', \
         'products': ['TechPro Ultrabook', 'BlueWave Gaming Laptop', 'PowerLite Convertible', \
                      'TechPro Desktop', 'BlueWave Chromebook']
        }
    ]
    """

    msgs = [
        {'role': 'system', 'content': system_msg},
        {'role': 'user', 'content': f"{delimiter}{few_shot_user_1}{delimiter}"},
        {'role': 'assistant', 'content': few_shot_assistant_1},
        {'role': 'user', 'content': f"{delimiter}{few_shot_user_2}{delimiter}"},
        {'role': 'assistant', 'content': few_shot_assistant_2},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"}
    ]

    response, think = get_completion_from_messages(msgs, model=model)
    return response


def eval_response_with_ideal(response : str, ideal, debug=False):
    if debug:
        print("Response: ", response)

    # json.loads() will convert the string to a dictionary
    l_of_d = json.loads(response.replace("'", "\""))

    # If the response is empty, that is none of the categories and products
    # are found.
    if l_of_d == [] and ideal == []:
        return 1
    # Another case is that the response and ideal results
    # are not compatible.
    elif l_of_d == [] or ideal == []:
        return 0

    # The correct response number.
    correct = 0

    if debug:
        print('l_of_d is ', l_of_d)

    # Process each response-ideal pair
    for d in l_of_d:

        # Acquire the category and products from the response
        cat = d.get('category')
        prod_1 = d.get('products')

        # If found the category and products
        if cat and prod_1:
            # convert list to set for comparison
            prod_set = set(prod_1)
            ideal_cat = ideal.get(cat)
            if ideal_cat:
                prod_set_ideal = set(ideal.get(cat))
            else:
                if debug:
                    print(f"No category found for {cat}")
                    print(f"The ideal answer: {ideal}")
                continue

            if debug:
                print("The product set:\n", prod_set)
                print()
                print("The ideal product set:\n", prod_set_ideal)

            # Compare the product set with the ideal product set
            if prod_set == prod_set_ideal:
                if debug:
                    print("Correct")
                correct += 1
            else:
                print("Incorrect")
                print("The product set: ", prod_set)
                print("The ideal product set: ", prod_set_ideal)
                if prod_set <= prod_set_ideal:
                    print("The response is a subset of the ideal product set")
                elif prod_set >= prod_set_ideal:
                    print("The response is a superset of the ideal product set")

    # compute the ratio of correctness.
    return correct / len(l_of_d)


class TestQAV2(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()
        if not os.path.exists('products.json'):
            create_products()
        self.products_and_category = get_products_and_category()

    def test_process_user_message(self):
        customer_msg = f"""
        Tell me about the smartx pro phone and the fotosnap camera, the dslr one.
        Also, what TVs do you have?"""

        response_v2 = find_category_and_product_v2(customer_msg, self.products_and_category, model=self.model)

        pprint(json.loads(response_v2.replace('\'', '\"')))


def eval_with_rubric(test_set, assistant_answer, model):
    cust_msg = test_set['customer_msg']
    context = test_set['context']
    completion = assistant_answer

    # The prompt for answer correctness evaluation
    system_msg = """
    You are an assistant that evaluates how well the customer service agent \
    answers a user question by looking at the context that the customer service \
    agent is using to generate its response.
    """

    # The commands
    user_msg = f"""
    You are evaluating a submitted answer to a question based on the context \
    that the agent uses to answer the question.
    
    Here is the data:
    [BEGIN DATA]
    ************
    [QUESTION]: {cust_msg}
    ************
    [CONTEXT]: {context}
    ************
    [SUBMISSION]: {completion}
    ************
    [END DATA]
    
    Compare the factual content of the submitted answer with the context. \
    Ignore any differences in style, grammar, or punctuation.
    Answer the following questions:
        - Is the Assistant response based only on the context provided? (Y or N)
        - Does the answer include information that is not provided in the context? (Y or N)
        - Is there any disagreement between the response and the context? (Y or N)
        - For each question that the user asked, is there a corresponding answer to it?
            Question 1: (Y or N)
            Question 2: (Y or N)
            ...
            Question N: (Y or N)
        - Of the number of questions asked, how many of these questions were addressed \
          by the answer? (output a number)
    """

    msgs = [
        {'role': 'system', 'content': system_msg},
        {'role': 'user', 'content': user_msg}
    ]

    response, _ = get_completion_from_messages(msgs, model=model)

    return response


test_set_ideal = {
'customer_msg': """\
tell me about the smartx pro phone and the fotosnap camera, the dslr one.
Also, what TVs or TV related products do you have?"""
,
'ideal_answer':"""\
Of course! The SmartX ProPhone is a powerful \
smartphone with advanced camera features. \
For instance, it has a 12MP dual camera. \
Other features include 5G wireless and 128GB storage. \
It also has a 6.1-inch display. The price is $899.99.
The FotoSnap DSLR Camera is great for \
capturing stunning photos and videos. \
Some features include 1080p video, \
3-inch LCD, a 24.2MP sensor, \
and interchangeable lenses. \
The price is 599.99.
For TVs and TV related products, we offer 3 TVs \
All TVs offer HDR and Smart TV.
The CineView 4K TV has vibrant colors and smart features. \
Some of these features include a 55-inch display, \
'4K resolution. It's priced at 599.
The CineView 8K TV is a stunning 8K TV. \
Some features include a 65-inch display and \
8K resolution. It's priced at 2999.99
The CineView OLED TV lets you experience vibrant colors. \
Some features include a 55-inch display and 4K resolution. \
It's priced at 1499.99.
We also offer 2 home theater products, both which include bluetooth.\
The SoundMax Home Theater is a powerful home theater system for \
an immmersive audio experience.
Its features include 5.1 channel, 1000W output, and wireless subwoofer.
It's priced at 399.99.
The SoundMax Soundbar is a sleek and powerful soundbar.
It's features include 2.1 channel, 300W output, and wireless subwoofer.
It's priced at 199.99
Are there any questions additional you may have about these products \
that you mentioned here?
Or may do you have other questions I can help you with?
"""
}


def eval_vs_ideal(test_set, assistant_answer, model):
    cus_msg = test_set['customer_msg']
    ideal = test_set['ideal_answer']
    completion = assistant_answer

    system_msg = """
    You are an assistant that evaluates how well the customer service agent \
    answers a user question by comparing the response to the ideal (expert) \
    response.
    
    Output a single letter and nothing else.
    """

    user_msg = f"""
    You are comparing a submitted answer to an expert answer on a given question.
    Here is the data:
    [BEGIN DATA]
    ************
    [QUESTION]: {cus_msg}
    ************
    [EXPERT]: {ideal}
    ************
    [SUBMISSION]: {completion}
    ************
    [END DATA]
    
        Compare the factual of the submitted answer with the expert answer. \
    Ignore any differences in style, grammar, or punctuation.
        The submitted answer may either be a subset or superset of the expert answer, \
    or it may conflict with it. Determine which case applies.
        Answer the question by selecting one of the following options:
        - A: The submitted answer is a subset of the expert answer and is fully consistent with it.
        - B: The submitted answer is a superset of the expert answer and is fully consistent with it.
        - C: The submitted answer contains all the same details as the expert answer.
        - D: There is a disagreement between the submitted answer and the expert answer.
        - E: The answers differ, but these differences don't matter from the persepective of factuality.
        
        choice_strings: ABCDE
    """

    msgs = [
        {'role': 'system', 'content': system_msg},
        {'role': 'user', 'content': user_msg}
    ]

    response, think = get_completion_from_messages(msgs, model=model)
    return response


class TestUncertenedQA(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()
        if not os.path.exists('products.json'):
            create_products()
        self.products_and_category = get_products_and_category()

    def test_process_user_message(self):
        customer_msg = f"""
        Tell me about the smartx pro phone and the fotosnap camera, the dslr one.
        Also, what TVs or TV related products do you have?"""

        # Extract the products from the customer message
        products_by_category = get_products_from_query(customer_msg)

        # Convert the products to a list
        category_and_product_list = read_string_to_list(products_by_category)

        # Query product info
        product_info = get_mentioned_product_info(category_and_product_list)

        # Generate answer for the user message
        assistant_answer = answer_user_msg(user_msg=customer_msg, product_info=product_info)

        print(assistant_answer)

        # Evaluate the response with LLM model.

        # question and context
        cust_prod_info = {
            'customer_msg':customer_msg,
            'context': product_info
        }

        evaluation_output = eval_with_rubric(cust_prod_info, assistant_answer, self.model)
        print("\n\n\n", evaluation_output)

    def test_process_user_message_2(self):
        customer_msg = f"""
        Tell me about the smartx pro phone and the fotosnap camera, the dslr one.
        Also, what TVs or TV related products do you have?"""

        # Extract the products from the customer message
        products_by_category = get_products_from_query(customer_msg)

        # Convert the products to a list
        category_and_product_list = read_string_to_list(products_by_category)

        # Query product info
        product_info = get_mentioned_product_info(category_and_product_list)

        # Generate answer for the user message
        assistant_answer = answer_user_msg(user_msg=customer_msg, product_info=product_info)

        evaluation_output = eval_vs_ideal(test_set_ideal, assistant_answer, self.model)
        print("\n\n\n", evaluation_output)

        assistant_answer_2 = "life is like a box of chocolates."
        evaluation_output_2 = eval_vs_ideal(test_set_ideal, assistant_answer_2, self.model)
        print("\n\n\n\n", evaluation_output_2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
