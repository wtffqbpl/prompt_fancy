#! coding: utf-8

from enum import Enum
from applications.chatbot.memory import get_user_memory, save_user_memory, save_chat_history


class DialogState(Enum):
    """
    Enum to represent the state of the dialog.
    """
    WELCOME = "welcome"
    ORDERING = "ordering"
    PAYMENT = "payment"
    CONFIRMATION = "confirmation"
    END = "end"


def determine_state(user_input):
    if 'order' in user_input.lower():
        return DialogState.ORDERING
    elif 'pay' in user_input.lower():
        return DialogState.PAYMENT
    elif 'confirm' in user_input.lower():
        return DialogState.CONFIRMATION
    else:
        return DialogState.WELCOME


def build_prompt(user_id, user_input, state):
    memory = get_user_memory(user_id)
    prompt = f"""
    You are a customer service assistant. Here is the user's information:
    - Name: {memory.get('name', 'Unknown')}
    - Address: {memory.get('address', 'Unknown')}
    - Recent history: {memory.get('history', [])}
    
    Current conversation state: {state.value}
    User said: {user_input}
    
    Please generate a natural response based on the above information.
    """
    return prompt

