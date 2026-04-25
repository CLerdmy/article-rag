import requests

from llm.base import BaseLLM


class GeminiLLM(BaseLLM):

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash-lite"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def generate(self, prompt: str) -> str:

        url = (
            f"{self.base_url}/models/"
            f"{self.model}:generateContent"
        )

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        request = requests.post(
            url,
            params={"key": self.api_key},
            json=payload
        )

        request.raise_for_status()
        data = request.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]