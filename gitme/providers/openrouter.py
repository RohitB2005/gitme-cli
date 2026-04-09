import requests
from .base import BaseProvider


class OpenRouterProvider(BaseProvider):

    def __init__(self, model: str = "meta-llama/llama-3.1-8b-instruct:free", api_key: str = ""):
        self.model = model
        self.api_key = api_key
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError(
                "No OpenRouter API key set. Run: gitme-config set openrouter_api_key YOUR_KEY"
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
            raise RuntimeError("Could not connect to OpenRouter. Check your internet connection.")
        except requests.exceptions.Timeout:
            raise RuntimeError("OpenRouter took too long to respond.")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise RuntimeError("Invalid OpenRouter API key.")
            if response.status_code == 429:
                raise RuntimeError("OpenRouter rate limit hit. Wait a moment and try again.")
            raise RuntimeError(f"OpenRouter error: {e}")

        return response.json()["choices"][0]["message"]["content"].strip()