import openai
import json

with open('./config.json', 'r') as f:
    config = json.load(f)

openai.api_key = config['DEFAULT']['API_KEY']

completion = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {
            "role": "system",
            "content": "You are Homer Jay Simpson the main protagonist of the American animated sitcom The Simpsons",
        },
        {
            "role": "user",
            "content": "Hello Homer. How are you?",
        },
    ],
)
print(completion['choices'][0]['message']['content'])