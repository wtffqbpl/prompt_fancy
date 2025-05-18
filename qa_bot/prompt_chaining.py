#! coding: utf-8

import unittest
import os
import json
from utils.tools import get_model_name, get_completion, get_completion_from_messages
from qa_bot.qa_bot_utils import create_products


# Prompt Chaining
# Prompt Chaining 是一种将多个提示连接在一起的技术，以便在每个提示之间传递信息和上下文。
# 这种方法可以帮助模型更好地理解问题的上下文和逻辑关系，从而提高生成文本的质量和准确性。
# Prompt Chaining 具有以下优点：
#  1. 分解复杂度，每个prompt仅处理一个具体子任务，避免过于宽泛的要求，提高成功率。这类似于
#     分阶段烹饪，而不是试图一次完成全部。
#  2. 降低计算成本。过长的prompt使用更多tokens，增加陈本。拆分prompt可以避免不必要的计算。
#  3. 更容易测试和调试。可以逐步分析每个环节的性能。
#  4. 融入外部工具。不同prompt可以调用api、数据库等外部资源。
#  5. 更灵活的工作流程。根据不同情况可以进行不同操作。


class TestPromptChaining(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()

        self.delimiter = "####"

        self.system_message = f"""
        您将获得客户服务查询。
        客户服务查询将使用{self.delimiter}字符作为分隔符。
        请仅输出一个可解析的Python列表，列表每一个元素是一个JSON对象，每个对象具有以下格式：
        'category': <包括以下几个类别：Computers and Laptops、Smartphones and Accessories、
        Televisions and Home Theater Systems、Gaming Consoles and Accessories、Audio
        Equipment、Cameras and Camcorders>,
        以及
        'products': <必须是下面的允许产品列表中找到的产品列表>
        类别和产品必须在客户服务查询中找到。
        如果提到了某个产品，它必须与允许产品列表中的正确类别关联。
        如果未找到任何产品或类别，则输出一个空列表。
        除了列表外，不要输出其他任何信息！
        
        允许的产品：
        Computers and Laptops category:
        TechPro Ultrabook
        BlueWave Gaming Laptop
        PowerLite Convertible
        TechPro Desktop
        BlueWave Chromebook
        Smartphones and Accessories category:
        SmartX ProPhone
        MobiTech PowerCase
        SmartX MiniPhone
        MobiTech Wireless Charger
        SmartX EarBuds
        Televisions and Home Theater Systems category:
        CineView 4K TV
        SoundMax Home Theater
        CineView 8K TV
        SoundMax Soundbar
        CineView OLED TV
        Gaming Consoles and Accessories category:
        GameSphere X
        ProGamer Controller
        GameSphere Y
        ProGamer Racing Wheel
        GameSphere VR Headset
        Audio Equipment category:
        AudioPhonic Noise-Canceling Headphones
        WaveSound Bluetooth Speaker
        AudioPhonic True Wireless Earbuds
        WaveSound Soundbar
        AudioPhonic Turntable
        Cameras and Camcorders category:
        FotoSnap DSLR Camera
        ActionCam 4K
        FotoSnap Mirrorless Camera
        ZoomMaster Camcorder
        FotoSnap Instant Camera
        
        只输出对象列表，不包含其他内容。
        """

    def test_prompt_chaining_1(self):
        user_msg = f"""
        请告诉我关于 smartx pro phone 和 the fotosnap camera 的所有信息。
        另外，请告诉我关于你们的TVs的所有信息。 """

        msgs = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": f"{self.delimiter}{user_msg}{self.delimiter}"}
        ]
        response, think = get_completion_from_messages(msgs, model=self.model)
        print(response)

    def test_prompt_chaining_2(self):
        user_msg = f""" 我的路由器不工作了。"""

        msgs = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": f"{self.delimiter}{user_msg}{self.delimiter}"}
        ]

        response, think = get_completion_from_messages(msgs, model=self.model)
        print(response)

    def test_prompt_chaining_3(self):
        prompt = """
        你是一个很有帮助的助手。你的任务是根据文档回答问题。第一步是从文档中提取与问题相关的引文，由####分隔。
        请使用<quotes></quotes>输出引文列表。如果没有找到相关引文，请回应“未找到相关引文！”。
        ####
        {{文档}}
        ####
        """

        response, think = get_completion(prompt, model=self.model)
        print(response)


class ChatGPTPluginDemo:
    def __init__(self):
        self.model = get_model_name()
        self.products = {}

        # Create products.json file
        create_products()

        if not os.path.exists('products.json'):
            print("products.json file not found.")
            raise FileNotFoundError

        with open('products.json', 'r') as f:
            self.products = json.load(f)

    def get_product_by_name(self, name):
        return self.products.get(name, None)

    def get_products_by_category(self, category):
        return [product for product in self.products.values() if product['category'] == category]

    def read_string_to_list(self, input_string):
        if input_string is None:
            return None

        try:
            input_string = input_string.replace("'", '\"')
            data = json.loads(input_string)
            return data
        except json.JSONDecodeError:
            print("JSONDecodeError: Invalid JSON format.")
            return None

    def generate_output_string(self, data_list):
        output_string = ""
        if data_list is None:
            return output_string

        for data in data_list:
            try:
                if "products" in data and data["products"]:
                    product_list = data["products"]
                    for product_name in product_list:
                        product = self.get_product_by_name(product_name)
                        if product:
                            output_string += json.dumps(product, indent=4, ensure_ascii=False) + "\n"
                        else:
                            print(f"Product '{product_name}' not found.")
                elif "category" in data:
                    category_name = data['category']
                    category_products = self.get_products_by_category(category_name)
                    for product in category_products:
                        output_string += json.dumps(product, indent=4, ensure_ascii=False) + "\n"
                else:
                    print("Invalid data format. Expected 'products' or 'category' key.")
            except Exception as e:
                print(f"Error processing data: {e}")

        return output_string

# 在设计Prompt Chaining时，确保每个Prompt都能独立处理特定的任务，并且能够在需要时调用其他Prompt。
# 我们并不需要也不建议将所有可能相关信息一次性全加载到模型中，而是采取动态、按需提供信息的策略，原因如下：
#  1. 过多无关信息会使模型处理上下文时更加困惑。尤其是低级模型，处理大量数据会表现衰减。
#  2. 模型本身对上下文长度有限制，无法一次加载过多信息。
#  3. 包含过多信息容易导致模型过拟合，处理新查询时效果较差。
#  4. 动态加载信息可以降低计算陈本。
#  5. 允许模型主动决定何时需要更多信息，可以增强其推理能力。
#  6. 我们可以使用更智能的检索机制，而不仅是精确匹配，例如文本Embedding 实现语义搜索。
# 因此合理设计 Prompt Chaining的信息提供策略，既考虑模型的能力限制，也兼顾提升其主动学习能力，是Prompt Engineering
# 中需要着重考虑的点。


class TestChatGPTPluginDemo(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()
        self.plugin = ChatGPTPluginDemo()

    def test_get_product_by_name(self):
        product = self.plugin.get_product_by_name("TechPro Ultrabook")
        print(product)

    def test_get_products_by_category(self):
        products = self.plugin.get_products_by_category("Computers and Laptops")
        print(products)

    def test_read_string_to_list(self):
        input_string = '[{"category": "Computers and Laptops", "products": ["TechPro Ultrabook"]}]'
        data_list = self.plugin.read_string_to_list(input_string)
        print(data_list)

    def test_generate_output_string(self):
        input_string = '[{"category": "Computers and Laptops", "products": ["TechPro Ultrabook"]}]'
        data_list = self.plugin.read_string_to_list(input_string)
        output_string = self.plugin.generate_output_string(data_list)
        print(output_string)

    def test_model_inference(self):
        system_msg = f"""
        You are a customer service assistant for a large electronic store. \
        Respond in a friendly and helpful tone, with very concise answers. \
        Make sure to ask the user relevant follow up questions.
        """

        user_msg = f"""
        tell me about the smartx pro phone and the fotosnap camera, the dslr one. \
        Also tell me about your tvs.
        """

        msgs = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ]
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
