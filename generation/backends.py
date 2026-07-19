import ollama
import os

def generate_ollama(prompt: str, model: str = "qwen3.5:9b") -> str:
    response = ollama.generate(model=model, prompt=prompt)
    return response["response"]

def generate_openai(prompt: str, model: str = "gpt-4o-mini") -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_anthropic(prompt: str, model: str = "claude-sonnet-4-6") -> str:
    from anthropic import Anthropic
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

BACKENDS = {
    "ollama": generate_ollama,
    "openai": generate_openai,
    "anthropic": generate_anthropic,
}

def generate(prompt: str, backend: str = "ollama", **kwargs) -> str:
    return BACKENDS[backend](prompt, **kwargs)