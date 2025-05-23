# Prompt Fancy

Prompt Fancy is a comprehensive project dedicated to exploring and implementing various techniques in prompt engineering and natural language processing. It provides a collection of tools, modules, and applications designed to demonstrate the power and versatility of large language models. The project includes examples of sentiment analysis, information extraction, topic inference, a functional chatbot application, and a question answering bot capable of handling product-related queries. It also integrates with LangChain for enhanced LLM interactions and chain-of-thought reasoning.

## Features

- **Advanced Inference Capabilities:** Comprehensive examples of text analysis including sentiment analysis, emotion detection, information extraction, and topic inference.
- **Chatbot Application:** A FastAPI-based chatbot that uses dialog management, memory (Redis for short-term, PostgreSQL for long-term), and interacts with a language model to provide responses.
- **Prompt Engineering Techniques:** Examples and explanations of core prompt engineering principles, including using delimiters, seeking structured output, giving the model time to think, and few-shot prompting.
- **Question Answering Bot:** A bot capable of processing user queries, identifying relevant products and categories from a predefined list, retrieving product information, and generating informative responses.
- **LangChain Integration:** Integration with LangChain for enhanced LLM interactions, chain-of-thought reasoning, and modular prompt development.
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

- **Inference Examples:** Explore various text analysis capabilities in `inference.py`, including sentiment analysis, emotion detection, and topic inference.
- **Applications/Chatbot:** Run the chatbot application. See `applications/chatbot/app.py` for details.
- **Prompt Engineering:** Explore examples and principles of prompt engineering. See the files within the `prompt_engineering` directory for specific examples.
- **QA Bot:** Learn how to build a Question Answering bot. See `qa_bot/bot.py` and `qa_bot/qa_bot_utils.py` for implementation details.
- **LangChain Module:** Explore LangChain integration examples and utilities in the `langchain_module` directory.
- **Utils:** Explore general utility functions used across the project. See `utils/tools.py` and `utils/configs.py`.

## Project Structure

```
.
├── .gitignore
├── .env
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
├── langchain_module/
│   ├── __init__.py
│   ├── bases.py
│   ├── memory.py
│   ├── memory_new_api.py
│   └── model_chain.py
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

## File Descriptions

### Root Directory
- `inference.py`: Core file containing examples of text analysis capabilities including sentiment analysis, emotion detection, information extraction, and topic inference. Includes comprehensive test cases demonstrating various prompt engineering techniques.

### Applications/Chatbot
- `app.py`: FastAPI application implementing the chatbot interface with endpoints for chat interactions and web interface.
- `config.py`: Configuration settings for the chatbot application including database connections and model parameters.
- `dialog_manager.py`: Manages conversation flow and state, handling user input and generating appropriate responses.
- `memory.py`: Implements both short-term (Redis) and long-term (PostgreSQL) memory storage for chat history and user context.

### LangChain Module
- `bases.py`: Base classes and interfaces for LangChain integration, providing core functionality for chain operations.
- `memory.py`: Implementation of LangChain memory components for storing and retrieving conversation history.
- `memory_new_api.py`: Updated memory implementation using the latest LangChain API.
- `model_chain.py`: Chain implementations for model interactions and prompt processing.

### Prompt Engineering
- `chatbox.py`: Interactive chat interface for testing and demonstrating prompt engineering techniques.
- `iterative_prompt_devel.py`: Examples and utilities for iterative prompt development and refinement.
- `prompt_principles.py`: Comprehensive collection of prompt engineering principles and best practices.
- `summarize.py`: Implementation of various text summarization techniques using LLMs.
- `text_transformation.py`: Tools and examples for text transformation tasks like translation, style transfer, and format conversion.
- `writing.py`: Examples and utilities for AI-assisted writing tasks.

### QA Bot
- `bot.py`: Main implementation of the question-answering bot with product query handling.
- `classification.py`: Product and category classification utilities for the QA bot.
- `cot.py`: Chain-of-thought reasoning implementations for complex question answering.
- `evaluate_result.py`: Tools for evaluating and validating QA bot responses.
- `input_audit.py`: Input validation and sanitization utilities.
- `llm_tokens.py`: Token management and optimization utilities.
- `llm_unittest_policies.py`: Unit testing framework and policies for LLM interactions.
- `prompt_chaining.py`: Implementation of prompt chaining techniques for complex reasoning.
- `qa_bot_utils.py`: Core utilities and helper functions for the QA bot.

### Utils
- `configs.py`: Global configuration settings and environment variables management.
- `tools.py`: General-purpose utility functions used across the project.

## Dependencies

The project uses several key dependencies:
- OpenAI API (v1.77) for language model interactions
- FastAPI (v0.115.12) for the web application
- Redis (v6.0.0) and SQLAlchemy (v2.0.40) for data storage
- LangChain (v0.3.25) and LangChain Community (v0.3.24) for enhanced LLM interactions
- Panel (v1.6.3) for UI components
- Various utility libraries:
  - rich (v13.9.4) for terminal formatting
  - redlines (v0.5.1) for text comparison
  - selenium (v4.32.0) for web automation
  - pandas (v2.2.3) for data manipulation
  - tenacity (v8.5.0) for retry logic

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

[Include license information here, e.g., MIT, Apache 2.0]
