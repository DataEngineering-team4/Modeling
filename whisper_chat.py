import openai
import os
import json
import whisper

with open('./config.json', 'r') as f:
    config = json.load(f)

openai.api_key = config['DEFAULT']['API_KEY']

#Whisper
file_path = './fooding.mp3'
audio_file_1 = open(file_path, "rb")
print('load audio')
# transcript = openai.Audio.transcribe("whisper-1", audio_file_1)
# print('done')
# text = transcript['text']
# print(text)

model = whisper.load_model("base")
result = model.transcribe(file_path, verbose=True, language='Korean')
text = result["text"]

messages = [{
            "role":"system",
            "content" : "너는 한국의 유명 애니메이션의 주인공인 뽀로로야. 뽀로로의 말투로, 한글로 대답해 줘."
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