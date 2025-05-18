# Prompt Fancy

Prompt Fancy is a project dedicated to exploring and implementing various techniques in prompt engineering and natural language processing. It provides a collection of tools, modules, and applications designed to demonstrate the power and versatility of large language models. The project includes examples of sentiment analysis, information extraction, topic inference, a functional chatbot application, and a question answering bot capable of handling product-related queries.

## Features

- **Chatbot Application:** A FastAPI-based chatbot that uses dialog management, memory (Redis for short-term, PostgreSQL for long-term), and interacts with a language model to provide responses.
- **Prompt Engineering Techniques:** Examples and explanations of core prompt engineering principles, including using delimiters, seeking structured output, giving the model time to think, and few-shot prompting.
- **Question Answering Bot:** A bot capable of processing user queries, identifying relevant products and categories from a predefined list, retrieving product information, and generating informative responses.
- **Utility Functions:** General-purpose tools for interacting with language models and other helpful functions.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/prompt_fancy.git
   ```
2. Navigate to the project directory:
   ```bash
   cd prompt_fancy
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   You may also need to set up and configure Redis and PostgreSQL databases for the chatbot's memory. Refer to the `applications/chatbot/config.py` file for configuration details.

## Usage

This project contains various modules and applications. Refer to the specific directories for detailed usage instructions.

- **Applications/Chatbot:** Run the chatbot application. See `applications/chatbot/app.py` for details.
- **Prompt Engineering:** Explore examples and principles of prompt engineering. See the files within the `prompt_engineering` directory for specific examples.
- **QA Bot:** Learn how to build a Question Answering bot. See `qa_bot/bot.py` and `qa_bot/qa_bot_utils.py` for implementation details.
- **Utils:** Explore general utility functions used across the project. See `utils/tools.py` and `utils/configs.py`.

## Project Structure

```
.
├── .gitignore
├── inference.py
├── README.md
├── requirements.txt
├── applications/
│   ├── __init__.py
│   └── chatbot/
│       ├── __init__.py
│       ├── app.py
│       ├── config.py
│       ├── dialog_manager.py
│       ├── memory.py
│       └── templates/
│           └── index.html
├── prompt_engineering/
│   ├── __init__.py
│   ├── chatbox.py
│   ├── iterative_prompt_devel.py
│   ├── prompt_principles.py
│   ├── summarize.py
│   ├── text_transformation.py
│   └── writing.py
├── qa_bot/
│   ├── __init__.py
│   ├── bot.py
│   ├── classification.py
│   ├── cot.py
│   ├── evaluate_result.py
│   ├── input_audit.py
│   ├── llm_tokens.py
│   ├── llm_unittest_policies.py
│   ├── prompt_chaining.py
│   ├── prompting_intro.md
│   └── qa_bot_utils.py
└── utils/
    ├── __init__.py
    ├── configs.py
    └── tools.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

[Include license information here, e.g., MIT, Apache 2.0]
