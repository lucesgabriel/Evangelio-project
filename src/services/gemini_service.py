import google.generativeai as genai
from termcolor import colored
from config.config import GEMINI_API_KEY

class GeminiAPI:
    def __init__(self):
        try:
            print(colored("Initializing Gemini API...", "yellow"))
            genai.configure(api_key=GEMINI_API_KEY)
            self.generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 65536,
            }
            self.model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-thinking-exp-01-21",
                generation_config=self.generation_config,
            )
            print(colored("✓ Gemini API initialized", "green"))
        except Exception as e:
            print(colored(f"Error initializing Gemini API: {str(e)}", "red"))
            raise

    def generate_text(self, prompt):
        """
        Generates text using Gemini API
        """
        try:
            print(colored("Generating text with Gemini...", "yellow"))
            response = self.model.generate_content(prompt)
            print(colored("✓ Text generated successfully", "green"))
            return response.text
        except Exception as e:
            print(colored(f"Error generating text: {str(e)}", "red"))
            raise 