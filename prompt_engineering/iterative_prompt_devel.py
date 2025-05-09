#! coding: utf-8

import unittest
from rich.console import Console
from rich.markdown import Markdown
from utils.tools import get_model_name, get_completion, show_html_content

"""
Iterative Prompt Development
    Iterative process
        * Try something.
        * Analyze where the result does not give what you want.
        * Clarify instructions, give more time to think.
        * Refine prompts with a batch of examples.
"""


class TestIterativePromptDevelopment(unittest.TestCase):
    def setUp(self) -> None:
        self.model = get_model_name()

        self.console = Console()

        self.fact_sheet_chair = """
OVERVIEW
- Part of a beautiful family of mid-century inspired office furniture,
including filing cabinets, desks, bookcases, meeting tables, and more.
- Several options of shell color and base finishes.
- Available with plastic back and front upholstery (SWC-100)
or full upholstery (SWC-110) in 10 fabric and 6 leather options.
- Base finish options are: stainless steel, matte black,
gloss white, or chrome.
- Chair is available with or without armrests.
- Suitable for home or business settings.
- Qualified for contract use.
CONSTRUCTION
- 5-wheel plastic coated aluminum base.
- Pneumatic chair adjust for easy raise/lower action.
DIMENSIONS
- WIDTH 53 CM | 20.87”
- DEPTH 51 CM | 20.08”
- HEIGHT 80 CM | 31.50”
- SEAT HEIGHT 44 CM | 17.32”
- SEAT DEPTH 41 CM | 16.14”
OPTIONS
- Soft or hard-floor caster options.
- Two choices of seat foam densities:
medium (1.8 lb/ft3) or high (2.8 lb/ft3)
- Armless or 8 position PU armrests
MATERIALS
SHELL BASE GLIDER
- Cast Aluminum with modified nylon PA6/PA66 coating.
- Shell thickness: 10 mm.
SEAT
- HD36 foam
COUNTRY OF ORIGIN
- Italy
        """

    def test_iterative_prompt_development(self):
        # Example of a prompt that could be improved
        prompt = f"""
        Your task is to help a marketing team create a description
        for a retail website of a product based on a technical fact sheet.
        
        Write a product description based on the information
        provided in the technical specifications delimited by
        triple backticks.
        
        AND THE OUTPUT SHOULD BE IN MARKDOWN FORMAT.
        
        Use at most 50 words.
        
        Technical specifications: ```{self.fact_sheet_chair}```
        """

        # Simulate getting a response from the model
        response, think = get_completion(prompt, model=self.model)

        self.console.print(Markdown(response))

        # print(response)

    def test_iterative_prompt_development_2(self):
        # Example of a prompt that could be improved
        prompt = f"""
        Your task is to help a marketing team create a description
        for a retail website of a product based on a technical fact sheet.
        
        Write a product description based on the information
        provided in the technical specifications delimited by
        triple backticks.
        
        The description is intended for furniture retailers,
        so should be technical in nature and focus on the
        materials the product is constructed from.
        
        Use at most 50 words.
        
        Technical specifications: ```{self.fact_sheet_chair}```
        """

        # Simulate getting a response from the model
        response, think = get_completion(prompt, model=self.model)

        print(response)

    def test_iterative_prompt_development_3(self):
        # Example of a prompt that could be improved
        prompt = f"""
        Your task is to help a marketing team create a description
        for a retail website of a product based on a technical fact sheet.
        
        Write a product description based on the information
        provided in the technical specifications delimited by
        triple backticks.
        
        The description is intended for furniture retailers,
        so should be technical in nature and focus on the
        materials the product is constructed from.
        
        At the end of the description, include every 7-character
        Product ID in the technical specification with the following format:
        Product IDs: <Product IDs>
        
        Use at most 50 words.
        
        Technical specifications: ```{self.fact_sheet_chair}```
        """

        # Simulate getting a response from the model
        response, think = get_completion(prompt, model=self.model)

        print(response)

    def test_iterative_prompt_development_4(self):
        # Example of a prompt that could be improved
        prompt = f"""
        Your task is to help a marketing team create a description
        for a retail website of a product based on a technical fact sheet.
        
        Write a product description based on the information
        provided in the technical specifications delimited by
        triple backticks.
        
        The description is intended for furniture retailers,
        so should be technical in nature and focus on the
        materials the product is constructed from.
        
        At the end of the description, include every 7-character
        Product ID in the technical specification with the following format:
        Product IDs: <Product IDs>
        
        After the description, include a table that gives the
        product's dimensions. The table should have two columns.
        In the first column include the name of the dimension.
        In the second column include the measurements in inches only.
        
        For the *product description*, please do not use markdown format to
        format the text, use HTML instead.
        
        Give the table the title 'Product Dimensions'.
        
        Format everything as HTML that can be used in a website.
        Place the description in a <div> tag.
        
        Technical specifications: ```{self.fact_sheet_chair}```
        """

        # Simulate getting a response from the model
        response, think = get_completion(prompt, model=self.model)

        print(response)
        show_html_content(response)


if __name__ == '__main__':
    unittest.main(verbosity=2)
