import requests
import json

gemini_api_key = "AIzaSyBK3qPmHS-IPj5pd1YC8Dir4UTqDoC7GV0"

def get_completion(messages, model="gemini-1.0-pro", temperature=1.0, max_tokens=1000):
    payload = {
        "contents": messages,
        "generationConfig": {
            "temperature": temperature, "maxOutputTokens": max_tokens
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
    }
    response = requests.post(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_api_key}', data=json.dumps(payload))
    obj = json.loads(response.text)
    if response.status_code == 200:
        return obj["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return obj["error"]

def handle_user_input(input):
    messages = []

    for i in range(len(input)):
        if i % 2 == 0:
            messages.append({
                "role": "user",
                "parts": [
                    {
                        "text": input[i]
                    }
                ]
            })
        else:
            messages.append({
                "role": "model",
                "parts": [
                    {
                        "text": input[i]
                    }
                ]
            })

    response = get_completion(messages=messages, model="gemini-1.0-pro", temperature=0.5)

    return response