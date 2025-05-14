#! coding: utf-8
import sys
import unittest
import subprocess
import socket
import os
import threading
import time
import panel as pn  # GUI
from utils.tools import get_model_name, get_completion, get_completion_from_messages

pn.extension()


class ChatBoxTest(unittest.TestCase):

    def setUp(self) -> None:
        self.model = get_model_name()

    def test_tell_jokes(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant that speaks like Shakespeare."},
            {"role": "user", "content": "Tell me a joke."},
            {'role': 'assistant', 'content': "Why did the chicken cross the road? To get to the other side!"},
            {'role': 'user', 'content': "I don't get it."},
        ]

        response, think = get_completion_from_messages(messages, model=self.model, temperature=1)
        print(response)
        print(think)

    def test_friendly_chatbot(self):
        messages = [
            {'role': 'system', 'content': 'You are a friendly chatbot.'},
            {'role': 'user', 'content': 'Hi, my name is Isa'}
        ]

        response, _ = get_completion_from_messages(messages, model=self.model, temperature=1)
        print(response)

    def test_chatbot_interactive(self):
        panels = []  # Collect display
        context = [
            {'role': 'system',
             'content': """You are OrderBot, an automated service to collect orders for a pizza restaurant. \
                           You first greet the customer, then collects the order, \
                           and then asks if it's a pickup or delivery. \
                           You wait to collect the entire order, then summarize it and check for a final \
                           time if the customer wants to add anything else. \
                           If it's a delivery, you ask for an address. \
                           Finally you collect the payment.\
                           Make sure to clarify all options, extras and sizes to uniquely \
                           identify the item from the menu.\
                           You respond in a short, very conversational friendly style. \
                           The menu includes \
                           pepperoni pizza 12.95, 10.00, 7.00 \
                           cheese pizza 10.95, 9.25, 6.50 \
                           eggplant pizza 11.95, 9.75, 6.75 \
                           fries 4.50, 3.50 \
                           greek salad 7.25 \
                           Toppings: \
                           extra cheese 2.00, \
                           mushrooms 1.50 \
                           sausage 3.00 \
                           canadian bacon 3.50 \
                           AI sauce 1.50 \
                           peppers 1.00 \
                           Drinks: \
                           coke 3.00, 2.00, 1.00 \
                           sprite 3.00, 2.00, 1.00 \
                           bottled water 5.00 \
                           """
             }
        ]  # accumulate messages

        while True:
            try:
                user_input = input("User: ").strip()
            except KeyboardInterrupt:
                print('\nExiting chat...')
                sys.exit(0)

            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break

            # Add user input to context
            context.append({'role': 'user', 'content': user_input})

            # Get response from model
            response, think = get_completion_from_messages(context, model=self.model, temperature=0.7)

            # add response to context
            context.append({'role': 'assistant', 'content': response})

            # Display the response
            print(f"Assistant: {response}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
