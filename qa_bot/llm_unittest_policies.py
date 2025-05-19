#! coding: utf-8

import unittest
import os
import json
from pprint import pprint
from utils.tools import get_model_name, get_completion_from_messages
from qa_bot.qa_bot_utils import (
    create_products,
    get_products_and_category
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
    # The another case is that the response and ideal results
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
