# File: list_models.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def list_available_models():
    """Lists all available models and prints their names."""
    print("Fetching available models...")
    models = genai.list_models()
    available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]

    if not available_models:
        print("No models found that support generateContent.")
        print("Please check your API key and network connection.")
        return

    print("\nAvailable models for your project:")
    for model_name in available_models:
        print(f"- {model_name}")

if __name__ == "__main__":
    list_available_models()