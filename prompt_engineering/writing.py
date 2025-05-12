#! coding: utf-8

import unittest
from utils.tools import get_model_name, get_completion


class LLMWritingPromptTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()

        self.review = f"""
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

        self.sentiment_prompt = """
        What is the sentiment of the following product review, which is
        delimited with triple backticks?
        
        Give your answer as a single word, either "positive", "neutral" or "negative".
        
        ONLY RETURN THE SENTIMENT, DO NOT RETURN ANY OTHER TEXT.
        
        Review text: ```{review}```
        """

        self.prompt = """
        You are a customer service AI assistant.
        Your task is to send an email reply toa valued customer.
        Given the customer email delimited by ```, \
        Generate a reply to thank the customer for their review.
        If the sentiment is positive or neutral, thank them for \
        their review.
        If the sentiment is negative, apologize and suggest that \
        they can reach out to customer service.
        Make sure to use specific details from the review.
        Write in a concise and professional tone.
        Sign the email as `AI customer agent`.
        Customer review: ```{review}```
        Review sentiment: {sentiment}
        """

    def test_write_email(self):
        # Get the sentiment of the review
        sentiment_prompt = self.sentiment_prompt.format(review=self.review)
        sentiment, _ = get_completion(sentiment_prompt, model=self.model)

        print(sentiment)

        email_prompt = self.prompt.format(
            review=self.review,
            sentiment=sentiment
        )

        response, think = get_completion(email_prompt, model=self.model)
        print(response)
        print(think)

    def test_write_email_with_temperature(self):
        # Get the sentiment of the review
        sentiment_prompt = self.sentiment_prompt.format(review=self.review)
        sentiment, _ = get_completion(sentiment_prompt, model=self.model)

        print(sentiment)

        # Generate the email reply
        email_prompt = self.prompt.format(
            review=self.review,
            sentiment=sentiment
        )
        response, think = get_completion(email_prompt, model=self.model, temperature=0.7)
        print(response)
        print(think)


if __name__ == '__main__':
    unittest.main(verbosity=2)
