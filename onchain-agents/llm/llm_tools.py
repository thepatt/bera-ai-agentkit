from dotenv import load_dotenv
import os
from openai import OpenAI
from transformers import pipeline
import google.generativeai as genai

load_dotenv()

# Configure LLM clients using keys from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
flan_t5_model = pipeline("text2text-generation", model="google/flan-t5-small")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = "gemini-1.5-flash"


def process_with_openai(prompt, system_prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error with OpenAI: {e}"


def process_with_flan_t5(prompt, system_prompt):
    try:
        combined_prompt = f"{system_prompt}\n\n{prompt}"
        response = flan_t5_model(combined_prompt, max_length=256)
        return response[0]["generated_text"].strip()
    except Exception as e:
        return f"Error with Hugging Face FLAN-T5: {e}"


def process_with_gemini(prompt, system_prompt):
    try:
        combined_prompt = f"{system_prompt}\n\n{prompt}"
        response = genai.generate_text(
            model=gemini_model, prompt=combined_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error with Google Gemini: {e}"
