import requests

url = "https://mobilex.kr/ai/dev/team4/predict/inference"

# 요청 페이로드
payload = {
    "input_text": "안녕하세요, 테스트 메시지입니다.",
    "text2mel_model": "fastspeech2",
    "vocoder_model": "mb_melgan"
}

# POST 요청 보내기
response = requests.post(url, json=payload)

# 응답 확인
if response.status_code == 200:
    data = response.json()
    mel_outputs = data["mel_outputs"]
    audio = data["audio"]
    print("Mel outputs:", mel_outputs)
    print("Audio:", audio)
else:
    print("Request failed with status code:", response.status_code)

