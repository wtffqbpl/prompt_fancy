# Prompt Fancy

Prompt Fancy is a project dedicated to exploring and implementing various techniques in prompt engineering and natural language processing. It provides a collection of tools, modules, and applications designed to demonstrate the power and versatility of large language models. The project includes examples of sentiment analysis, information extraction, topic inference, a functional chatbot application, and a question answering bot capable of handling product-related queries.

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

## Usage

This project contains various modules and applications. Refer to the specific directories for detailed usage instructions.

- **Applications:** Contains example applications built using prompt engineering techniques.
- **Prompt Engineering:** Contains modules and examples related to prompt engineering principles and techniques.
- **QA Bot:** Contains modules and examples for building a Question Answering bot.
- **Utils:** Contains utility functions used across the project.

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
│       ├── model_handler.py
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
│   ├── classification.py
│   ├── cot.py
│   ├── evaluate_result.py
│   ├── input_audit.py
│   ├── llm_tokens.py
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
