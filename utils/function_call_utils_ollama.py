#! coding: utf-8


import re
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import json
from typing import Callable, Dict, List, Optional, Union


def get_response(text: str) -> str:
    """ Remove the <think>...</think> tags from the text and return the remaining content. """
    # Match the <think> tag and its content (supports multi-line)
    pattern = re.compile(r'<think>(.*?)</think>', re.DOTALL)
    match = pattern.search(text)

    if match:
        # Remove the <think>...</think> part and keep the rest
        answer_content = pattern.sub('', text).strip()
    else:
        answer_content = text.strip()

    return answer_content


class Tool:
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description

    def to_dict(self) -> Dict[str, Union[str, Callable]]:
        return {
            "name": self.name,
            "description": self.description,
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": json.dumps({
                    "type": "object",
                    "properties": {},
                    "required": []
                })
            }
        }

    def call(self, args: Dict) -> str:
        return self.func(**args)


class FunctionCallSimulator:
    def __init__(self, model_name: str, temperature: float = 0.2):
        self.tools: Dict[str, Tool] = {}
        self.llm = Ollama(model=model_name, temperature=temperature)

        # Prompt template for function calling
        self.template = """
        You are an assistant that can choose to call the following tools based on the question:
        {tools_desc}
        
        IF YOU NEED TO CALL A TOOL, RETURN A JSON OBJECT IN THE FOLLOWING FORMAT WITHOUT ANY ADDITIONAL CONTENT:
        [
            {{"name": "tool_name1", "arguments": {{"argument1": "value1", "argument2": "value2"}}}},
            {{"name": "tool_name2", "arguments": {{"argument1": "value1", "argument2": "value2"}}}},
        ]
        ADDITIONALLY, PLEASE ENSURE THAT THE RESPONSE IS A VALID JSON STRING.
        SO BEFORE RETURNING THE RESPONSE, MAKE SURE TO CALL json.dumps() ON THE RESPONSE.
        
        question: {question}
        """

        self.prompt = PromptTemplate.from_template(self.template)

    def register_tool(self, tool: Tool):
        """ Registers a tool to the simulator."""
        self.tools[tool.name] = tool

    def _generate_tools_description(self) -> str:
        """ Generates a description of all registered tools."""
        if not self.tools:
            return "No tools available."

        desc = ""
        for tool in self.tools.values():
            desc += f"- {tool.name}: {tool.description}\n"

        return desc.strip()

    def run(self, question: str) -> list[str]:
        tools_desc = self._generate_tools_description()
        input_prompt = self.prompt.format(tools_desc=tools_desc, question=question)
        res = self.llm.invoke(input_prompt).strip()
        print(res)
        response = get_response(res)

        try:
            tool_calls = json.loads(response)

            if isinstance(tool_calls, dict):
                tool_calls = [tool_calls]

            results = []
            for tool_call in tool_calls:
                tool_name = tool_call.get("name")
                arguments = tool_call.get("arguments", {})

                if tool_name not in self.tools:
                    raise ValueError(f"Invalid tool name: {tool_name}")

                tool = self.tools[tool_name]
                result = tool.call(arguments)
                results.append(result)
            return results
        except json.JSONDecodeError:
            return ["Invalid response format." +\
                " Please ensure the response is a valid JSON string." +\
                response]


if __name__ == '__main__':
    def get_weather(location: str):
        return f"The weather in {location} is sunny with a high of 25°C."

    def search_wikipedia(query: str) -> str:
        return f"The Wikipedia page for {query} is very informative."

    # Initialize the function call simulator
    simulator = FunctionCallSimulator(model_name="qwen3:8b")

    # Register tools
    simulator.register_tool(Tool(name="get_weather", func=get_weather, description="Get the weather"))
    simulator.register_tool(Tool(name="search_wikipedia", func=search_wikipedia, description="Search Wikipedia"))

    # Example question
    question = "What is the weather in Paris? And tell me about Python programming language."

    # Run the simulator
    response = simulator.run(question)
    print("The response from the function call simulator:")
    print(response)
