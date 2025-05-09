#! coding: utf-8

import unittest
from utils.tools import get_model_name, get_completion


class TestPromptForSummarization(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()
        self.review_1 = f"""
        Got this panda plush toy for my daughter's birthday, \
        who loves it and takes it everywhere. It's soft and \
        super cute, and its face has a friendly look. It's \
        a bit small for what I paid though. I think there \
        might be other options that are bigger for the \
        same price. It arrived a day earlier than expected, \
        so I got to play with it myself before I gave it to her.
        """

        # review for a standing lamp
        self.review_2 = """
        Needed a nice lamp for my bedroom, and this one \
        had additional storage and not too high of a price \
        point. Got it fast - arrived in 2 days. The string \
        to the lamp broke during the transit and the company \
        happily sent over a new one. Came within a few days \
        as well. It was easy to put together. Then I had a \
        missing part, so I contacted their support and they \
        very quickly got me the missing piece! Seems to me \
        to be a great company that cares about their customers \
        and products.
        """
        # review for an electric toothbrush
        self.review_3 = """
        My dental hygienist recommended an electric toothbrush, \
        which is why I got this. The battery life seems to be \
        pretty impressive so far. After initial charging and \
        leaving the charger plugged in for the first week to \
        condition the battery, I've unplugged the charger and \
        been using it for twice daily brushing for the last \
        3 weeks all on the same charge. But the toothbrush head \
        is too small. I’ve seen baby toothbrushes bigger than \
        this one. I wish the head was bigger with different \
        length bristles to get between teeth better because \
        this one doesn’t. Overall if you can get this one \
        around the $50 mark, it's a good deal. The manufacture's \
        replacements heads are pretty expensive, but you can \
        get generic ones that are more reasonably priced. This \
        toothbrush makes me feel like I've been to the dentist \
        every day. My teeth feel sparkly clean!
        """

        # review for a blender
        self.review_4 = """
        So, they still had the 17 piece system on seasonal \
        sale for around $49 in the month of November, about \
        half off, but for some reason (call it price gouging) \
        around the second week of December the prices all went \
        up to about anywhere from between $70-$89 for the same \
        system. And the 11 piece system went up around $10 or \
        so in price also from the earlier sale price of $29. \
        So it looks okay, but if you look at the base, the part \
        where the blade locks into place doesn’t look as good \
        as in previous editions from a few years ago, but I \
        plan to be very gentle with it (example, I crush \
        very hard items like beans, ice, rice, etc. in the \
        blender first then pulverize them in the serving size \
        I want in the blender then switch to the whipping \
        blade for a finer flour, and use the cross cutting blade \
        first when making smoothies, then use the flat blade \
        if I need them finer/less pulpy). Special tip when making \
        smoothies, finely cut and freeze the fruits and \
        vegetables (if using spinach-lightly stew soften the \
        spinach then freeze until ready for use-and if making \
        sorbet, use a small to medium sized food processor) \
        that you plan to use that way you can avoid adding so \
        much ice if at all-when making your smoothie. \
        After about a year, the motor was making a funny noise. \
        I called customer service but the warranty expired \
        already, so I had to buy another one. FYI: The overall \
        quality has gone done in these types of products, so \
        they are kind of counting on brand recognition and \
        consumer loyalty to maintain sales. Got it in about \
        two days.
        """

    def test_fact_sheet(self):

        prompt = f"""
        Your task is to generate a short summary of a product \
        review from an ecommerce site.
        
        Summarize the review below, delimited by triple backticks,
        in at most 30 words.
        
        Review: ```{self.review_1}```
        """

        result, think = get_completion(prompt, model=self.model)
        print(result)

    def test_summarization_2(self):
        # 侧重于快递服务

        prompt = f"""
        Your task is to generate a short summary of a product \
        review from an ecommerce site to give feedback to the \
        shipping department.
        
        Summarize the review below, delimited by triple backticks, \
        in at most 30 words, and focusing on any aspects \
        that mention shipping and delivery of the product.
        
        Review: ```{self.review_1}```
        """

        result, think = get_completion(prompt, model=self.model)
        print(result)

    def test_summarization_3(self):
        # 侧重于价格和质量

        prompt = f"""
        Your task is to generate a short summary of a product \
        review from an ecommerce site to give feedback to the \
        shipping department, responsible for determining the \
        price of the product.
        
        Summarize the review below, delimited by triple backticks, \
        in at most 30 words, and focusing on any aspects \
        that are relevant to the price and perceived value.
        
        Review: ```{self.review_1}```
        """

        result, think = get_completion(prompt, model=self.model)
        print(result)

    def test_summarization_4(self):
        # 关键信息提取

        prompt = f"""
        Your task is to generate a short summary of a product \
        review from an ecommerce site to give feedback to the \
        shipping department.
        
        From the review below, delimited by triple quotes \
        extract the information relevant to shipping and delivery. \
        Limit to 30 words.
        
        Review: ```{self.review_1}```
        """

        result, think = get_completion(prompt, model=self.model)
        print(result)

    def test_summarize_multiple_reviews(self):
        reviews = [self.review_1, self.review_2, self.review_3, self.review_4]

        for i, review in enumerate(reviews):
            prompt = f"""
            Your task is to generate a short summary of a product \
            review from an ecommerce site.
            
            Summarize the review below, delimited by triple backticks \
            in **AT MOST 20 WORDS**.
            
            PLEASE SUMMARIZE EACH REVIEW, MULTIPLE REVIEWS HAVE NO RELATIONSHIP, \
            AND PLEASE DO NOT OUTPUT SINGLE WORDS.
            
            Review: ```{review}```
            """

            response, think = get_completion(prompt, model=self.model)
            print(i, response, "\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)
