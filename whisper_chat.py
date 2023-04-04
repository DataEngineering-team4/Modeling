import openai
import os
import json
import whisper

with open('./config.json', 'r') as f:
    config = json.load(f)

openai.api_key = config['DEFAULT']['API_KEY']

#Whisper
file_path = './4_5631.wav'
audio_file_1 = open(file_path, "rb")
print('load audio')

model = whisper.load_model("base")

result = model.transcribe(file_path, verbose=False, language='Korean') # if you use CPU, then give 'fp16=False' option
text = result["text"]

messages = [{
            "role":"system",
            "content" : "노는 것을 제일 좋아하는 개구쟁이 5살 아이의 말투로 대답해 줘."
        },]

message = text
if message:
    messages.append(
        {"role": "user", "content": message},
    )
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages,
    )

reply = chat.choices[0].message.content
print(f"뽀로로: {reply}")
messages.append({"role": "assistant", "content": reply})