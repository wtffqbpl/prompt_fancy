#! coding: utf-8

import unittest
from utils.tools import get_completion
from utils.tools import get_model_name

"""
Prompt设计技巧
1. 使用分隔符清晰地表示输入的不同部分
    分隔符就像是Prompt中的墙，将不同的部分隔开，帮助模型更好地理解输入的结构和内容。
    可以使用 ```, \"\"\", <>, <tag> </tag> : 等作为分隔符, 只要能明确起到隔断作用即可。
    
    使用分隔符可以防止 提示词注入(Prompt Rejection), 即用户输入的内容被模型误解为提示词的一部分。

2. 寻求结构化输出
    结构化输出可以帮助模型更好地理解和处理信息。
    例如，要求模型以JSON格式返回结果，或者使用表格、列表等形式组织输出。
    
    结构化输出可以提高模型的可读性和可解析性，便于后续处理和分析。


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


if __name__ == '__main__':
    unittest.main(verbosity=2)
