# clients/groq_client.py

from groq import Groq

class GroqClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

        self.client = Groq(api_key=api_key)

        # Available models
        self.allowed_models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]

    def reply(self, user_input: str, system_context: str, tone: str, model_name: str) -> str:
        messages = [
            {"role": "system", "content": f"{system_context}\nTone: {tone}"},
            {"role": "user", "content": user_input}
        ]

        completion = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.7
        )

        return completion.choices[0].message.content
