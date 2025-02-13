from transformers import pipeline

google_llm = pipeline("text2text-generation", model="google/flan-t5-small")


def process_with_google(prompt):
    try:
        google_prompt = (
            "You are a helpful assistant. "
            "Please interpret the content below and provide a concise response:\n"
            f"{prompt}"
        )
        response = google_llm(google_prompt, max_length=256)
        return response[0]["generated_text"].strip()
    except Exception as e:
        return f"Error with Google LLM: {e}"
