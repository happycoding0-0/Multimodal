
import whisper
from path import model_download_root
import sounddevice as sd
import openwakeword 
from openwakeword.model import Model


class Stt():
    def __init__(self):
        self.SAMPLE_RATE = 16000
        
        self.stt_model = whisper.load_model(name = "small", download_root=model_download_root, in_memory=True)

        openwakeword.utils.download_models(target_directory=f"{model_download_root}/openwakeword_models")
        self.wakeword_model = Model(
            wakeword_models=[f"{model_download_root}/openwakeword_models/hey_jarvis_v0.1.onnx"],
            melspec_model_path=f"{model_download_root}/openwakeword_models/melspectrogram.onnx",
            embedding_model_path=f"{model_download_root}/openwakeword_models/embedding_model.onnx",
            inference_framework="onnx"
            )

    def wake_word(self):
        
        self.prediction = self.wakeword_model.predict(audio)
        
    def get_audio(self,duration = 5):
        print("recording...")
        self.audio = sd.rec(
            int(duration* self.SAMPLE_RATE),
            samplerate=self.SAMPLE_RATE,
            channels=1,
            dtype="float32"
                            )
        sd.wait()
        print("end recording")
        return self.audio.flatten()
    def stt(self):
        audio = self.get_audio(duration= 5)

        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio, n_mels=self.stt_model.dims.n_mels).to(self.stt_model.device)
        _, probs = self.stt_model.detect_language(mel)
        options = whisper.DecodingOptions()
        result = whisper.decode(self.stt_model, mel, options)
        print(result.text)

if __name__ == "__main__":
    stt = Stt()
    #print(f"{model_download_root}/openwakeword_models/hey_jarvis_v0.1.onnx")

    
    