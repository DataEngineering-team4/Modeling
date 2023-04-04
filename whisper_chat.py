import openai
import os
import json
import whisper

with open('./config.json', 'r') as f:
    config = json.load(f)

openai.api_key = config['DEFAULT']['API_KEY']

# g2pk
def natural_g2pk(text):
    from g2pk import G2p
    g2p = G2p()
    
    sent_set = text.split()
    output = []
    for word in sent_set:
        output.append(g2p(word))
    
    return (' '.join(output))

# Whisper
file_path = './4_5631.wav'
audio_file_1 = open(file_path, "rb")
print('load audio')

model = whisper.load_model("base")

result = model.transcribe(file_path, verbose=False, language='Korean', fp16=False) # if you use CPU, then give 'fp16=False' option
text = result["text"]
print(f'유저: {text}')

with open('./messages.json') as message_file:
    messages = json.load(message_file)

print(messages)

message = text
if message:
    messages['messages'].append(
        {"role": "user", "content": message},
    )
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages['messages'],
    )

reply = chat.choices[0].message.content
print(reply)
voice = natural_g2pk(reply)
print(f"뽀로로: {voice}")

messages['messages'].append({"role": "assistant", "content": reply})
with open('./messages.json', 'w') as outfile:
    json.dump(messages, outfile, indent=2)