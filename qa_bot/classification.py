#! coding: utf-8

import unittest
from utils.tools import get_model_name, get_completion, get_completion_from_messages


class TestLLMClassification(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()

        self.delimiter = "###"

        self.system_message = f"""
            你将获得客户服务查询。
            每个客户服务查询都将用{self.delimiter}字符分隔。
            将每个查询分类到一个主要类别和一个次要类别中。
            以 JSON 格式提供你的输出，包含以下键：primary 和 secondary。
            主要类别：计费（Billing）、技术支持（Technical Support）、账户管理（Account Management）
            或一般咨询（General Inquiry）。
            计费次要类别：
            取消订阅或升级（Unsubscribe or upgrade）
            添加付款方式（Add a payment method）
            收费解释（Explanation for charge）
            争议费用（Dispute a charge）
            技术支持次要类别：
            常规故障排除（General troubleshooting）
            设备兼容性（Device compatibility）
            软件更新（Software updates）
            账户管理次要类别：
            重置密码（Password reset）
            更新个人信息（Update personal information）
            关闭账户（Close account）
            账户安全（Account security）
            一般咨询次要类别：
            产品信息（Product information）
            定价（Pricing）
            反馈（Feedback）
            与人工对话（Speak to a human）
        """

    def test_classification_1(self):
        user_msg = f"""我希望你删除我的个人资料和所有用户数据。"""
        msgs = [
            {'role': 'system', 'content': self.system_message},
            {'role': 'user', 'content': f"{self.delimiter}{user_msg}{self.delimiter}"},
        ]

        response, think = get_completion_from_messages(messages=msgs, model=self.model)

        print(response)

    def test_classification_2(self):
        user_msg = f"""告诉我更多关于你们的平板电脑的信息。"""

        msg = [
            {'role': 'system', 'content': self.system_message},
            {'role': 'user', 'content': f"{self.delimiter}{user_msg}{self.delimiter}"},
        ]
        response, think = get_completion_from_messages(messages=msg, model=self.model)
        print(response)
    pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
