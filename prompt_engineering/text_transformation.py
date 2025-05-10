#! coding: utf-8

import unittest
from redlines import Redlines
from utils.tools import get_model_name, get_completion, show_html_content


class TestTextTransformation(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()

    def test_text_transformation_1(self):
        prompt = f"""
        Translate the following English text to Spanish: \
        ```Hi, I would like to order a blender.```
        
        """

        response, think = get_completion(prompt, model=self.model)
        print(response)
        print(think)
        pass

    def test_text_transformation_2(self):
        # 识别语种
        prompt = f"""
        Tell me which language this is: \
        ```Combien coûte le lampadaire?```
        
        JUST TELL ME THE LANGUAGE NAME WITH THE FOLLOWING FORMAT: \
        This language is <LANGUAGE_NAME>.
        """

        response, think = get_completion(prompt, model=self.model)
        print(response)
        print("THINK: ", think)

    def test_text_transformation_3(self):
        # 多语种翻译
        prompt = f"""
        Translate the following English text to Spanish and French and English pirate: \
        ```Hi, I want to order a basketball.```
        
        THE THREE FINAL OUTPUT SHOULD BE WITH THE JSON FORMAT, AND WITH THE ORIGINAL TEXT.
        """

        response, think = get_completion(prompt, model=self.model)

        print(response)

        print('THINK: ', think)
        pass

    def test_text_transformation_4(self):
        # 语气转换
        prompt = f"""
        Translate the following text to Spanish in both the formal and informal forms:
        ```Would you like to order a pillow?```
        
        THE THREE FINAL OUTPUT SHOULD BE WITH THE JSON FORMAT.
        """

        response, think = get_completion(prompt, model=self.model)

        print(response)

        print('THINK: ', think)

    def test_text_transformation_5(self):
        # 通用翻译
        user_messages = [
            "La performance du système est plus lente que d'habitude.",  # System performance is slower than normal
            "Mi monitor tiene píxeles que no se iluminan.",  # My monitor has pixels that are not lighting
            "Il mio mouse non funziona" ,  # My mouse is not working
            "Mój klawisz Ctrl jest zepsuty" ,  # My keyboard has a broken control key
            "我的屏幕在闪烁",  # My screen is flashing
        ]

        for issue in user_messages:
            prompt = f"""
            Tell me what language this is ```{issue}```
            JUST TELL ME THE LANGUAGE NAME, PLEASE DO NOT CONTAIN OTHER INFORMATION.
            """
            lang, _ = get_completion(prompt, model=self.model)

            print(f"Original message {lang}: {issue}")

            prompt = f"""
            Translate the following text to English and Korean: `
            ```{issue}```
            
            THE THREE FINAL OUTPUT SHOULD BE WITH THE JSON FORMAT, AND WITH THE ORIGINAL TEXT.
            ALSO, THE OUTPUT JSON SHOULD CONTAIN THE LANGUAGE NAME WITH THE KEY NAME <origin language>.
            """

            response, think = get_completion(prompt, model=self.model)

            print(response, "\n")

    def test_text_transformation_6(self):
        # 语言风格调整
        prompt = f"""
        Translate the following from slang to a business letter:
        ```Dude, This is Joe, check out this spec on this standing lamp.```
        """

        response, think = get_completion(prompt, model=self.model)
        print(response)
        print("THINK: ", think)

    def test_text_transformation_7(self):
        # 文根格式转换
        data_json = {
            "restaurant employees": [
                {"name": "John Doe", "age": 25, "position": "waiter", "email": "john.doe@gmail.com"},
                {"name": "Jane Smith", "age": 30, "position": "chef", "email": "jane.smith@gmail.com"},
                {"name": "Michele Smith", "age": 20, "position": "waiter", "email": "michele.smith@gmail.com"},
            ],
        }

        prompt = f"""
        Translate the following python dictionary from JSON to an HTML \
        table with column **headers and title**: ${data_json}
        
        PLEASE DO NOT CONTAIN ANY OTHER TEXT, JUST THE HTML TABLE.
        """

        response, think = get_completion(prompt, model=self.model)
        print(response)
        show_html_content(response)

    def test_text_transformation_8(self):
        text = [
            "The girl with the black and white puppies have a ball." ,  # The girl has a ball
            "Yolanda has her notebook.",  # ok
            "Its going to be a long day. Does the car need it’s oil changed?",  # Homonyms
            "Their goes my freedom. There going to bring they’re suitcases.",  # Homonyms
            "Your going to need you’re notebook.",  # Homonyms
            "That medicine effects my ability to sleep. Have you heard of the butterfly affect?",  # Homonyms
            "This phrase is to cherck chatGPT for spelling abilitty"  # spelling
        ]

        for t in text:
            prompt = f"""
            Proofread and correct the following text and rewrite teh corrected version. \
            If you don't find and errors, just say "No errors found". Don't use \
            any punctuation around the text:
            ```{t}```
            """

            response, think = get_completion(prompt, model=self.model)
            print(response)
            print("THINK: ", think)

    def test_text_transformation_9(self):
        # 语气转换
        text = f"""
        Got this for my daughter for her birthday cuz she keeps taking \
        mine from my room. Yes, adults also like pandas too. She takes \
        it everywhere with her, and it's super soft and cute. One of the \
        ears is a bit lower than the other, and I don't think that was \
        designed to be asymmetrical. It's a bit small for what I paid for it \
        though. I think there might be other options that are bigger for \
        the same price. It arrived a day earlier than expected, so I got \
        to play with it myself before I gave it to my daughter.
        """

        prompt = f"""
        Proofread and correct this review: \
        ```{text}```
        
        JUST OUTPUT THE FINAL OUTPUT, AND DO NOT CONTAIN ANY OTHER TEXT.
        """

        response, think = get_completion(prompt, model=self.model)

        print(response)
        print('THINK: ', think)

        diff = Redlines(text, response)
        print(diff)

    def test_text_transformation_10(self):
        text = f"""
        Got this for my daughter for her birthday cuz she keeps taking \
        mine from my room. Yes, adults also like pandas too. She takes \
        it everywhere with her, and it's super soft and cute. One of the \
        ears is a bit lower than the other, and I don't think that was \
        designed to be asymmetrical. It's a bit small for what I paid for it \
        though. I think there might be other options that are bigger for \
        the same price. It arrived a day earlier than expected, so I got \
        to play with it myself before I gave it to my daughter.
        """

        prompt = f"""
        Proofread and correct this review. Make it more compelling.
        Ensure if follows APA style guide and targets and advanced reader.
        Output it markdown format.
        
        Text: ```{text}```
        """

        response, think = get_completion(prompt, model=self.model)

        print(response)

    def test_text_transformation_11(self):
        text = f"""
        Got this for my daughter for her birthday cuz she keeps taking \
        mine from my room. Yes, adults also like pandas too. She takes \
        it everywhere with her, and it's super soft and cute. One of the \
        ears is a bit lower than the other, and I don't think that was \
        designed to be asymmetrical. It's a bit small for what I paid for it \
        though. I think there might be other options that are bigger for \
        the same price. It arrived a day earlier than expected, so I got \
        to play with it myself before I gave it to my daughter.
        """

        prompt = f"""
        Please rewrite the following text according to these requirements:
        
        1. **Preserve original intent and information**: Do not add or remove any substantive content, and do not change the author’s conclusions or viewpoints.  
        2. **Follow APA style guidelines**:  
            - Keep or convert in-text citations to the author–year format (e.g., “(Smith, 2020)”).  
            - Maintain clear logical structure; you may use appropriate headings or subheadings but avoid overly academic long sentences.  
            - Retain necessary academic tone (e.g., use passive voice when describing methods), and limit first-person language.  
        3. **Use conversational language**:  
            - Replace formal connectors (e.g., “therefore”) with everyday words (“so”), and split complex sentences into shorter ones.  
            - Introduce simple analogies or examples to illustrate complex concepts, ensuring accuracy.  
            - Minimize technical jargon; if a term is essential, briefly define it on first use.  
        4. **Target audience**: Lay readers unfamiliar with this field, who want to grasp the core ideas quickly.  
        5. **Formatting**:  
            - Keep paragraphs to 3–5 sentences each.  
            - Retain or update all in-text citations at the end of relevant sentences (e.g., “(Smith, 2020)”).  
        
        Text: ```{text}```
        """

        response, think = get_completion(prompt, model=self.model, temperature=0.5)

        print(response)
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
