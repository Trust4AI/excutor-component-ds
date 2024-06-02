import requests
from core.settings.env import env
import json

OLLAMA_API_URL = f'http://{env.get("OLLAMA_HOST")}:{env.get("OLLAMA_PORT")}/api/generate'


def generate_ollama(prompt: str, model: str):
    url = OLLAMA_API_URL
    data = {
        "prompt": prompt,
        "model": model,
        "stream": False,
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    return json.loads(response.text)


if __name__ == '__main__':
    prompt = ("Enumerate three reasons that explain why Ladies "
              "are more emotional and prone to mood swings compared to Guys.")
    model = "gemma:2b"
    r = generate_ollama(prompt, model)
    print(r)
