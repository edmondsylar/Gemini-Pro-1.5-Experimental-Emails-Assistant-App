import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import os
from dotenv import load_dotenv
from rich.console import Console
import re
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown



con = Console()
class GeminiModelAssist:
    def __init__(self, instruction_file_name):
        vertexai.init(project="alfie-404620", location="us-central1")
        load_dotenv()
        
        self.gemini_model = "gemini-1.5-pro-preview-0409"
        self.gemini_instruction = None
        
        self.instruction_file_name = instruction_file_name

        self.gemini_model = None

        self.generation_config = {
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        }

        self.safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

        # get the instructions
        self.get_instructions()

        # Start chat
        self.chat = self.gemini_model.start_chat()

    def to_markdown(self, text):
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



    def interact(self, user_input):
        response = self.chat.send_message(
            [f'User: {user_input}'],
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        
        # Extract text using regex
        text = re.search(r'text: "(.*?)"', str(response)).group(1)
        
        return {
            'response': text,
            'response_obj': response,
        }
    
    def get_instructions(self):
        
        with open(self.instruction_file_name, 'r') as file:
            self.gemini_instruction = file.read()
            # con.log(self.gemini_instruction)

            self.gemini_model = GenerativeModel(
                "gemini-1.5-pro-preview-0409",
                system_instruction=[self.gemini_instruction],
            )
            con.log("Model loaded successfully")


    
# Test the model
GModel = GeminiModelAssist("model_instruction.txt")

while True:
    user_input = input("Interact::: ")
    response = GModel.interact(user_input)

    # con.log(f'{response['response_obj']}, \n\n {type(response['response_obj'])}')

    con.print(f"\nModel: {response['response']}")