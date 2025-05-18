#! coding: utf-8

import unittest
from utils.tools import get_model_name, get_completion_from_messages
from qa_bot.qa_bot_utils import (
    create_products,
    find_category_and_product_only,
    get_products_and_category,
    read_string_to_list,
    generate_output_string
)


def process_user_message(user_input, all_messages, model, debug=True):
    delimiter = "```"

    # TODO
    category_and_product_response = find_category_and_product_only(
        user_input,
        get_products_and_category())

    # Transform the response into a list
    category_and_product_list = read_string_to_list(category_and_product_response)

    if debug:
        print(f"Category and Product List: {category_and_product_list}")

    # Find the specific product info
    product_info = generate_output_string(category_and_product_list)
    if debug:
        print(f"Product Info: {product_info}")

    # Generate the response
    system_msg = f"""
    You are a customer service assistant for a large electronic store. \
    Respond in a friendly and helpful tone, with concise answers. \
    Make sure to ask the user relevant follow-up questions.
    """

    # Add the system message to the conversation
    msgs = [
        {'role': 'system', 'content': system_msg},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},
        {'role': 'assistant', 'content': f"Relevant product information:\n{product_info}"}
    ]

    response, think = get_completion_from_messages(all_messages + msgs, model=model)

    if debug:
        print(f"Response: {response}")
        print(f"Thinking Time: {think}")

    # Add the assistant's response to the conversation
    all_messages = all_messages + msgs[1:]

    # Check if the response is correct.
    user_msg = f"""
    Customer message: {delimiter}{user_input}{delimiter}
    Agent response: {delimiter}{response}{delimiter}
    
    Does the response sufficiently answer the customer's query?
    
    ONLY RESPOND WITH YES OR NO.
    """

    msgs = [
        {'role': 'system', 'content': system_msg},
        {'role': 'user', 'content': f"{delimiter}{user_msg}{delimiter}"}
    ]

    # Get the evaluation response
    evaluation_response, think = get_completion_from_messages(all_messages + msgs, model=model)
    if debug:
        print(f"Evaluation Response: {evaluation_response}")
        print(f"Evaluation Thinking Time: {think}")

    if "YES" in evaluation_response:
        if debug:
            print("The response is correct.")
        return response, all_messages
    else:
        if debug:
            print("The response is incorrect.")
        neg_str = "I'm sorry, we don't have that information. Can I help you with anything else?"
        return neg_str, all_messages


class QABotTest(unittest.TestCase):
    def setUp(self):
        create_products()
        self.model = get_model_name()

    def test_process_user_message(self):
        user_input = "Tell me about the SmartX Pro phone and the FotoSnap camera, the DSLR one. Also tell me about your TVs."
        all_messages = []
        response, all_messages = process_user_message(user_input, all_messages, self.model)
        print(f"Final Response: {response}")
        print(f"All Messages: {all_messages}")


    pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
