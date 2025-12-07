import requests
from app.config import OPENROUTER_API_KEY, OPENROUTER_MODEL

class LLMService:
    def ask(self, system_prompt: str, context: str, user_query: str):
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost",
            "X-Title": "FAQRehabBot",
            "Content-Type": "application/json"
        }

        payload = {
            "model": OPENROUTER_MODEL,
            "max_tokens": 200,  # <---- FIXED!
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "assistant", "content": context},
                {"role": "user", "content": user_query}
            ]
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)

            print("STATUS:", response.status_code)
            print("RAW:", response.text)

            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            return f"LLM Error: {str(e)}"
