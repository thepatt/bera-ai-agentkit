from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))  # Google API key loaded from .env
gemini_model = "gemini-1.5-flash"


def process_with_gemini(prompt):
    try:
        google_prompt = (
            "You are a helpful assistant. "
            "Please interpret the content below and provide a concise response:\n"
            f"{prompt}"
        )
        response = client.models.generate_content(
            model=gemini_model, contents=google_prompt
        )
        return response.text
    except Exception as e:
        return f"Error with Google Gemini: {e}"
