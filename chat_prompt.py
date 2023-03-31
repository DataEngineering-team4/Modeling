import openai
import json

from g2pk import G2p

g2p = G2p()

with open('./config.json', 'r') as f:
    config = json.load(f)

openai.api_key = config['DEFAULT']['API_KEY']

completion = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {
            "role": "system",
            "content": "너는 어린아이들을 가르치는 유치원 선생님이야. 어린아이에게 설명하듯이 대답해 줘",
            # "content": "You are Homer Jay Simpson the main protagonist of the American animated sitcom The Simpsons",
        },
        {
            "role": "user",
            "content": "선생님, 딥러닝이 뭐에요?",
        },
    ],
)

sent = completion['choices'][0]['message']['content']

print(sent)
print(g2p(sent))