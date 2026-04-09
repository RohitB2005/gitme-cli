import requests
from .base import BaseProvider

class OpenAIProvider(BaseProvider):

    def __init__(self, model: str = "gpt-4o-mini", api_key: str = ""):
        self.model = model
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/chat/completions"

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError(
                "No OpenAI API key set. Run: gitme-config set openai_api_key YOUR_KEY"
            )
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ]
        }

        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Could not connect to OpenAI. Check your internet connection.")
        except requests.exceptions.Timeout:
            raise RuntimeError("OpenAI took too long to respond.")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise RuntimeError("Invalid OpenAI API key.")
            if response.status_code == 429:
                raise RuntimeError("OpenAI rate limit hit. Wait a moment and try again.")
            raise RuntimeError(f"OpenAI error: {e}")

        return response.json()["choices"][0]["message"]["content"].strip()