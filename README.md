# Modeling

## 1. 내 목소리 데이터 준비

### 1-1. 음성 녹음

mimic-recording-studio 레포지토리 클론

```Shell
git clone https://github.com/pyrasis/mimic-recording-studio
```

필요 패키지 설치 (conda 기준)

```
conda create --name mimic python=3.8
conda activate mimic
conda install ffmpeg
cd mimic-recording-studio
cd backend
#WINDOW
pip install -r .\requirements.txt
#MAC: pip install -r requirements.txt
python run.py
```

Shell창 하나 더 열고 프론트엔드 실행

```
cd mimic-recording-studio
cd frontend
npm install #MAC 기준 호환성 문제 발생(npm install --force)로 해결
npm run start
```

웹 브라우저에 Mimic Recording Studio 표시된 이후

- 마이크 사용 권한 허용
- 이름 입력 (아무거나 상관 없음)
- Record 버튼 클릭해서 녹음 시작

<br>

음성 녹음 방법

1. 문장이 나오면 스페이스 눌러서 녹음 시작
2. 문장 다 읽은 후 기다리면 녹음 자동으로 종료 됨 (자동 종료 안될 경우 Esc)
   - 문장 잘못 읽어서 강제 종료 시키고 싶을 경우도 Esc
3. Review 버튼 클릭하면 녹음 들어볼 수 있음
   - 다시 녹음 하고 싶으면 스페이스바
4. 녹음 잘 되었으면 Next 클릭해서 다음 문장으로 이동

\* 주의사항: 일정한 속도로 읽기 / 문장부호 잘 구분 / 마이크 간격 일정하게 / 잡음 최대한 억제

<br>

### 1-2. 음성 데이터 정리

1. backend\audio_files\<UUID> 아래의 1, 2, 3, 4 폴더를 kss_myvoice\kss_myvoice 아래로 복사
2. backend\audio_files\transcript.v.1.4.txt 파일은 kss_myvoice 아래로 복사 (이전 위치보다 한단계 상위 폴더)

## 2. MFARunner로 TextGrid 생성

```
cd ~/
git clone https://github.com/pyrasis/MFARunner

conda activate mfa
conda config --add channels conda-forge
conda install montreal-forced-aligner==2.0.6
cd MFARunner
pip install -r requirements.txt
sudo apt-get install g++ openjdk-8-jdk python3-dev python3-pip curl
pip install konlpy==0.6.0 ffmpeg==1.4
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
```

```
# config.py
class Arguments:
        dataset_path = "data/kss_myvoice"

        preprocessed_file_dir = "./preprocessed"

        result_dir = "./result"
        phone_set = None

        num_jobs=8
```

```
python main.py
```

```
cd result/kss_myvoice
zip -r TextGrid.zip ./TextGrid
```

## 3. 내 목소리로 모델 학습

### 3-1. 경로 지정

```
conda activate tts
cd Korean-FastSpeech2-Pytorch
```

```
# hparams.py
import os
### kss ###
dataset = "kss_myvoice"
data_path = os.path.join("/mnt/c/data/kss_myvoice", dataset)
meta_name = "transcript.v.1.4.txt"      # "transcript.v.1.4.txt" or "transcript.v.1.3.txt"
textgrid_name = "TextGrid.zip"

... 생략 ...

# Vocoder
vocoder = None
vocoder_pretrained_model_name = "vocgan_kss_pretrained_model_epoch_4500.pt"
vocoder_pretrained_model_path = os.path.join("./vocoder/pretrained_models/", vocoder_pretrained_model_name)

... 생략 ...
```

### 3-2. 데이터 전처리

```
cp ../MFARunner/result/kss_myvoice/TextGrid.zip .
export LD_LIBRARY_PATH=/usr/lib/wsl/lib:$LD_LIBRARY_PATH
```

```
python preprocess.py
```

-> 수정 및 내용 추가 중
