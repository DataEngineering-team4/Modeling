import tensorflow as tf
from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor
from scipy.io.wavfile import write
import numpy as np

fastspeech2 = TFAutoModel.from_pretrained("tensorspeech/tts-fastspeech2-kss-ko", name="fastspeech2")
mb_melgan = TFAutoModel.from_pretrained("tensorspeech/tts-mb_melgan-kss-ko", name="mb_melgan")
processor = AutoProcessor.from_pretrained("tensorspeech/tts-fastspeech2-kss-ko")

def do_synthesis(input_text, text2mel_model, vocoder_model, text2mel_name, vocoder_name):
    input_ids = processor.text_to_sequence(input_text)
    # text2mel part
    mel_before, mel_outputs, duration_outputs, _, _ = text2mel_model.inference(
        tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
        speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
        speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
        f0_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
        energy_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
    )

    # vocoder part
    audio = vocoder_model.inference(mel_outputs)[0, :, 0]
    
    return mel_outputs.numpy(), audio.numpy()

input_text = "이것은 테스트입니다!"

if __name__ == "__main__":
    mels, audios = do_synthesis(input_text, fastspeech2, mb_melgan, "FASTSPEECH2", "MB-MELGAN")
    rate = 22050
    scaled = np.int16(audios / np.max(np.abs(audios)) * 32767)
    write('./wav_dir/test.wav', rate, scaled)