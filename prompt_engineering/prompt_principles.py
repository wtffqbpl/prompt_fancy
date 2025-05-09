#! coding: utf-8

import unittest
from utils.tools import get_completion
from utils.tools import get_model_name

"""
Principle 1: Write clear and specific instructions

Prompt设计技巧
1. 使用分隔符清晰地表示输入的不同部分
    Write clear and specific instructions
    分隔符就像是Prompt中的墙，将不同的部分隔开，帮助模型更好地理解输入的结构和内容。
    可以使用 ```, \"\"\", <>, <tag> </tag> : 等作为分隔符, 只要能明确起到隔断作用即可。
    Use delimiters to clearly indicate different parts of the input
    Triple quotes: \"\"\"
    Triple backticks: ```
    Triple dashes: ---
    Angle brackets: <>
    XML tags: <tag> </tag>
    
    使用分隔符可以防止 提示词注入(Prompt Rejection), 即用户输入的内容被模型误解为提示词的一部分。

2. 寻求结构化输出
    结构化输出可以帮助模型更好地理解和处理信息。
    例如，要求模型以JSON格式返回结果，或者使用表格、列表等形式组织输出。
    
    结构化输出可以提高模型的可读性和可解析性，便于后续处理和分析。

3. Give the model time to think
    Check whether conditions are satisfied. Check assumptions required to do the task.
    
4. Few-shot prompting
    Give successful examples of completing tasks, then ask model to perform the task.


"""


class TestPromptPrinciples(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()
        print(f"Model name: {self.model}")

    def test_prompt_with_delimiter(self):
        user_prompt = """
        你是一个专业的星座分析师。
        <user> 请简要分析双子座的性格特征和运势特点。 </user>
        """
        # 这里可以添加对提示词的验证逻辑
        self.assertIn("<user>", user_prompt)
        self.assertIn("</user>", user_prompt)
        self.assertIn("双子座", user_prompt)
        self.assertIn("性格特征", user_prompt)

        ans, think = get_completion(user_prompt, model=self.model, temperature=0.2)

        print(ans)

    def test_prompt_with_delimiter_2(self):
        text = f"""
        您应该提供尽可能清晰、具体的指示，以表达您希望模型执行的任务。\
        这将引导模型朝向所需的输出，并降低收到无关或不准确响应的风险。\
        不要讲写清晰地提示词与简短的提示词混淆。\
        在许多情况下，更长的提示词可以为模型提供更多上下文和信息，从而提高响应的质量。
        """

        # 需要总结的内容
        prompt = f"""
        把用三个反引号括起来的文本总结成一句话。
        ```{text}```
        """

        # 这里可以添加对提示词的验证逻辑
        self.assertIn("用三个反引号括起来的文本", prompt)

        # 调用模型获取总结
        summary, think = get_completion(prompt, temperature=0.2)
        print(summary)

    def test_prompt_with_delimiter_2_2(self):
        text = f"""
        You should express what you want a model to do by \
        providing instructions that are as clear and specific \
        as you can possibly make them. This will guide the model \
        towards the desired output, and reduce the chances of \
        receiving irrelevant or incorrect responses. Don't confuse \
        writing clear prompts with writing short prompts. In many \
        cases, longer prompts can provide the model with more \
        clarity and context for the model, which can lead to more \
        detailed and relevant outputs.
        """

        prompt = f"""
        Summarize the text delimited by triple backticks into a single sentence.
        ```{text}```
        """

        summary, think = get_completion(prompt, model=self.model, temperature=0.2)
        print(summary)

    def test_prompt_with_delimiter_3(self):
        prompt = f"""
        请生成包括书名、作者和类别的三本虚构的、非真实存在的中文书籍清单，\
        并以JSON格式提供，其中包含以下键: book_id, title, author, genre。\
        其中返回结果中只包含JSON内容，不需要其他额外信息，同时不需要增加```json
        这样的codeblock修饰。
        """

        summary, think = get_completion(prompt, model=self.model)

        print(summary)
        pass

    def test_prompt_with_structured_output(self):
        prompt = f"""
        Generate a list of three made-up book titles along \
        with their authors and genres.
        Provide them in JSON format with the following keys: \
        book_id, title, author, genre.
        """

        res, think = get_completion(prompt, model=self.model, temperature=0.2)
        print(res)

    def test_prompt_with_conditions_checking(self):
        text_1 = f"""
        Making a cup of tea is easy! First, you need to get some \
        water boiling. While that's happening, \
        grab a cup and put a tea bag in it. Once the water is \
        hot enough, just pour it over the tea bag. \
        Let it sit for a bit so the tea can steep. After a \
        few minutes, take out the tea bag. If you \
        like, you can add some sugar or milk to taste. \
        And that's it! You've got yourself a delicious \
        cup of tea to enjoy.
        """

        prompt = f"""
        You will be provided with text delimited by triple quotes. \
        If it contains a sequence of instructions, \
        re-write those instructions in a step-by-step format: \
        
        Step 1 - ...
        Step 2 - ...
        ...
        Step N - ...
        
        If the text does not contain a sequence of instructions, \
        then simply write \"No steps provided.\" \
        \"\"\"{text_1}\"\"\"
        """

        response, think = get_completion(prompt, model=self.model, temperature=0.2)
        print(response)

    def test_prompt_with_conditions_checking_2(self):
        text_2 = f"""
        The sun is shining brightly in the sky, and the birds are \
        singing. It's a beautiful day to go for a \
        walk in the park. The flowers are blooming, and the \
        trees are swaying gently in the breeze. People \
        are out and about, enjoying the lovely weather. \
        Some are having picnics, while others are playing \
        games or simply relaxing on the grass. It's a \
        perfect day to spend time outdoors and appreciate the \
        beauty of nature.
        """

        prompt = f"""
        You will be provided with text delimited by triple quotes. \
        If it contains a sequence of instructions, \
        re-write those instructions in a step-by-step format: \
        
        Step 1 - ...
        Step 2 - ...
        ...
        Step N - ...
        
        If the text does not contain a sequence of instructions, \
        then simply write \"No steps provided.\" \
        \"\"\"{text_2}\"\"\"
        """

        response, think = get_completion(prompt, model=self.model, temperature=0.2)
        print(response)

    def test_prompt_few_shot(self):
        # prompt = f"""
        # You are a professional astrologer. \
        # Please analyze the personality traits and fortune characteristics of Gemini.
        # """

        # ans, think = get_completion(prompt, model=self.model, temperature=0.2)
        # print(ans)

        prompt = f"""
        Your task is to answer in a consistent style.
        
        <child>: Teach me about patience.
        
        <grandparent>: The river that carves the deepest \
        valley flows from a modest spring; the \
        grandest symphony originates from a single note; \
        the most intricate tapestry begins with a solitary thread. \
        
        <child>: Teach me about resilience.
        """
        response, think = get_completion(prompt, model=self.model, temperature=0.2)
        print(response)


"""
Principle 2: Give the model time to think

Tactic 1: Specify the steps to complete a task.
    Step 1: ...
    Step 2: ...
    ...
    Step N: ...

Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion.
"""


class TestPromptPrinciple2(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()
        print(f"Model name: {self.model}")

    def test_prompt_with_think_time(self):
        text = f"""
        In a charming village, siblings Jack and Jill set out on \
        a quest to fetch water from a hilltop \
        well. As they climbed, singing joyfully, misfortune \
        struck-Jack tripped on a stone and bumbled \
        down the hill, will Jill following suit. \
        Though slightly battered, the pair returned home to \
        comforting embraces. Despite the mishap, \
        their adventurous spirits remained undimmed, and they \
        continued exploring with delight.
        """

        # example 1
        prompt_1 = f"""
        Perform the following actions:
        1 - Summarize the following text delimited by triple backticks with 1 sentence.
        2 - Translate the summary into French.
        3 - List each name in the French summary.
        4 - Output a json object that contains the following keys: french_summary, num_names.
        
        Perform the previous 4 actions, and separate 4 answers with line breaks.
        **AND YOU SHOULD ANSWER ALL 4 QUESTIONS.**
        
        
        Text:
        ```{text}```
        """

        ans, think = get_completion(prompt_1, model=self.model)
        print("Completion for prompt 1:")
        print(ans)

    def test_prompt_with_think_time_2(self):
        text = f"""
        In a charming village, siblings Jack and Jill set out on \
        a quest to fetch water from a hilltop \
        well. As they climbed, singing joyfully, misfortune \
        struck-Jack tripped on a stone and bumbled \
        down the hill, will Jill following suit. \
        Though slightly battered, the pair returned home to \
        comforting embraces. Despite the mishap, \
        their adventurous spirits remained undimmed, and they \
        continued exploring with delight.
        """

        # example 2
        prompt_2 = f"""
        Perform the following actions:
        1 - Summarize the following text delimited by <> with 1 sentence.
        2 - Translate the summary into French.
        3 - List each name in the French summary.
        4 - Output a json object that contains the following keys: french_summary, num_names.
        
        Use the following format:
        Text: <text to summarize>
        Summary: <summary>
        Translation: <summary translation>
        Names: <list of names in French summary>
        Output JSON: <json with summary and num_names>
        
        Text to summarize: <{text}>
        """

        ans, think = get_completion(prompt_2, model=self.model)
        print("Completion for prompt 2:")
        print(ans)

    def test_prompt_with_think_time_3(self):
        prompt = f"""
        Determine if the student's solution is correct or not.
        Question:
        I'm building a solar power installation and I need \
        help working out the financials.
        - Land costs $100 / square foot
        - I can buy solar panels for $250 / square foot
        - I negotiated a contract for maintenance that will cost \
        me a flat $100k per year, and an additional $10 / square \
        foot
        What is the total cost for the first year of operations
        as a function of the number of square feet.
        Student's Solution:
        Let x be the size of the installation in square feet.
        Costs:
        1. Land cost: 100x
        2. Solar panel cost: 250x
        3. Maintenance cost: 100,000 + 100x
        Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
        """

        ans, think = get_completion(prompt, model=self.model)
        print("Completion for prompt 3:")
        print(ans)
        print(think)

    def test_prompt_with_think_4(self):
        prompt = f"""
        Your task is to determine if the student's solution \
        is correct or not.
        To solve the problem do the following:
        - First, work out your own solution to the problem.
        - Then compare your solution to the student's solution \
        and evaluate if the student's solution is correct or not.
        Don't decide if the student's solution is correct until
        you have done the problem yourself.
        Use the following format:
        Question:
        question here
        ```
        Student's solution:
        ```
        student's solution here
        ```
        Actual solution:
        ```
        steps to work out the solution and your solution here
        ```
        Is the student's solution the same as actual solution \
        just calculated:
        ```
        yes or no
        ```
        Student grade:
        ```
        correct or incorrect
        ```
        Question:
        ```
        I'm building a solar power installation and I need help \
        working out the financials.
        - Land costs $100 / square foot
        - I can buy solar panels for $250 / square foot
        - I negotiated a contract for maintenance that will cost \
        me a flat $100k per year, and an additional $10 / square \
        foot
        What is the total cost for the first year of operations \
        as a function of the number of square feet.
        ```
        Student's solution:
        ```
        Let x be the size of the installation in square feet.
        Costs:
        1. Land cost: 100x
        2. Solar panel cost: 250x
        3. Maintenance cost: 100,000 + 100x
        Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
        Actual solution:
        """

        ans, think = get_completion(prompt, model=self.model)
        print(ans)


"""
Model Limitations

Hallucination (幻觉)
    The model may generate incorrect or nonsensical answers,
    especially when asked to perform complex tasks or provide
    detailed explanations.

Reducing hallucinations:
    1. Use few-shot prompting to provide examples of the desired output.
    2. Ask the model to check its own work.
    3. Ask the model to think step by step.
    4. Ask the model to explain its reasoning.
    5. Ask the model to verify its answer.
    6. Ask the model to provide sources for its information.
    
    First find relevant information,
    then answer the question based on the relevant information.
"""


class TestModelLimitations(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()
        print(f"Model name: {self.model}")

    def test_hallucination(self):
        prompt = f"""
        Tell me about AeroGlide UltraSlim Smart Toothbrush by Boie
        """

        ans, think = get_completion(prompt, model=self.model)
        print(ans)


if __name__ == '__main__':
    unittest.main(verbosity=2)
