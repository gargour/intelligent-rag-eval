from openai import OpenAI
from app.llm.base import BaseLLMClient
from app.config import get_settings

settings = get_settings()

class GrokClient(BaseLLMClient):
    def __init__(self, api_key: str = None):
        self.client = OpenAI(
            api_key=api_key or settings.grok_api_key,
            base_url=settings.grok_base_url,
        )
        self.model = settings.grok_model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=1500,
        )
        return response.choices[0].message.content

    def generate_stream(self, system_prompt: str, user_prompt: str):
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta