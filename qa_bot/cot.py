#! coding: utf-8

import unittest
from utils.tools import get_model_name, get_completion, get_completion_from_messages


# CoT (Chain-of-Thought)
# 在查询中明确要求语言模型先提供一系列相关推理步骤，进行深度思考，然后再给出最终答案，这种更接近人类解题的思维过程。
# 相比于直接要求输出结果，这种引导LLM进行思考的方式，能够显著提升模型的推理能力和准确性,
# 可以帮助模型更好地理解问题的上下文和逻辑关系。CoT 的关键在于引导模型进行深度思考和推理，而不是仅仅依赖于模型的记忆和模式匹配能力。
# CoT使语言模型更好地摸你人类逻辑思考，是提升模型推理能力的有效方法之一。


class TestPromptCoT(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()

        self.delimiter = "==="

        self.system_message = f"""
            请按照以下步骤回答客户的提问。客户的提问将以{self.delimiter}分隔。
            步骤 1:{self.delimiter}首先确定用户是否正在询问有关特定产品或产品的问题。产品类别不计入范围。
            步骤 2:{self.delimiter}如果用户询问特定产品，请确认产品是否在以下列表中。所有可用产品：
            
            产品：TechPro 超极本
            类别：计算机和笔记本电脑
            品牌：TechPro
            型号：TP-UB100
            保修期：1 年
            评分：4.5
            特点：13.3 英寸显示屏，8GB RAM，256GB SSD，Intel Core i5 处理器
            描述：
            一款适用于日常使用的时尚轻便的超极本。
            价格：$799.99
            
            产品：BlueWave 游戏笔记本电脑
            类别：计算机和笔记本电脑
            品牌：BlueWave
            型号：BW-GL200
            保修期：2 年
            评分：4.7
            特点：15.6 英寸显示屏，16GB RAM，512GB SSD，NVIDIA GeForce RTX 3060
            描述：
            一款高性能的游戏笔记本电脑，提供沉浸式体验。
            价格：$1199.99
            
            产品：PowerLite 可转换笔记本电脑
            类别：计算机和笔记本电脑
            品牌：PowerLite
            型号：PL-CV300
            保修期：1年
            评分：4.3
            特点：14 英寸触摸屏，8GB RAM，256GB SSD，360 度铰链
            描述：
            一款多功能可转换笔记本电脑，具有响应触摸屏。
            价格：$699.99
            
            产品：TechPro 台式电脑
            类别：计算机和笔记本电脑
            品牌：TechPro
            型号：TP-DT500
            保修期：1年
            评分：4.4
            特点：Intel Core i7 处理器，16GB RAM，1TB HDD，NVIDIA GeForce GTX 1660
            描述：
            一款功能强大的台式电脑，适用于工作和娱乐。
            价格：$999.99
            
            产品：BlueWave Chromebook
            类别：计算机和笔记本电脑
            品牌：BlueWave
            型号：BW-CB100
            保修期：1 年
            评分：4.1
            特点：11.6 英寸显示屏，4GB RAM，32GB eMMC，Chrome OS
            描述：
            一款紧凑而价格实惠的 Chromebook，适用于日常任务。
            价格：$249.99
            
            步骤 3:{self.delimiter} 如果消息中包含上述列表中的产品，请列出用户在消息中做出的任何假设，\
            例如笔记本电脑 X 比笔记本电脑 Y 大，或者笔记本电脑 Z 有 2 年保修期。
            步骤 4:{self.delimiter} 如果用户做出了任何假设，请根据产品信息确定假设是否正确。
            步骤 5:{self.delimiter} 如果用户有任何错误的假设，请先礼貌地纠正客户的错误假设（如果适用）。\
            只提及或引用可用产品列表中的产品，因为这是商店销售的唯一五款产品。以友好的口吻回答客户。
            使用以下格式回答问题：
            步骤 1: {self.delimiter} <步骤 1 的推理>
            步骤 2: {self.delimiter} <步骤 2 的推理>
            步骤 3: {self.delimiter} <步骤 3 的推理>
            步骤 4: {self.delimiter} <步骤 4 的推理>
            回复客户: {self.delimiter} <回复客户的内容>
            
            请确保每个步骤上面的回答中中使用 {self.delimiter} 对步骤和步骤的推理进行分隔。
        """

    def test_cot_1(self):
        user_message = f"""
            我想知道 TechPro 超极本的价格是多少？我听说它有 8GB 的内存和 256GB 的 SSD。
        """
        msg = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": user_message}
        ]
        response, think = get_completion_from_messages(msg, model=self.model)
        print(response)

    def test_cot_2(self):
        user_msg = f""" BlueWave Chromebook 比 TechPro 台式电脑贵多少？ """

        msgs = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": f"{self.delimiter}{user_msg}{self.delimiter}"}
        ]
        response, think = get_completion_from_messages(msgs, model=self.model)

        print(response)

    def test_cot_3(self):
        user_msg = "你有电视机么？"

        msgs = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": f"{self.delimiter}{user_msg}{self.delimiter}"}
        ]

        response, think = get_completion_from_messages(msgs, model=self.model)
        print(response)

    def test_cot_4(self):
        # 内心独白：
        #   内心独白技巧可以在一定程度上隐藏语言模型的推理过程，具体做法是，在prompt中指示语言模型以
        #   结构话格式存储需要隐藏的中间推理，例如存储为变量。然后在返回结果时，仅呈现对用户有价值的
        #   输出，不展示完整的推理过程。这种提示策略只向用户呈现关键信息，避免透露答案。同时语言模型的
        #   推理能力也得到保留。适当使用"内心独白"可以在保护敏感信息的同时，仍然保持语言模型的推理能力。

        user_msg = "我想知道 TechPro 超极本的价格是多少？我听说它有 8GB 的内存和 256GB 的 SSD。"
        msgs = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": f"{self.delimiter}{user_msg}{self.delimiter}"}
        ]

        response, think = get_completion_from_messages(msgs, model=self.model)

        print("ORIGIN: ", response)

        try:
            if self.delimiter in response:
                final_response = response.split(self.delimiter)[-1].strip()
            else:
                final_response = response.strip(":")[-1].strip()
        except Exception as e:
            final_response = "对不起，我现在有点问题，请尝试问另外一个问题。"

        print(final_response)


if __name__ == '__main__':
    unittest.main(verbosity=2)
