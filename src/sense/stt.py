import whisper
from path import model_download_root
import sounddevice as sd
class Stt():
    def __init__(self):
        self.model = whisper.load_model(name = "small", download_root=model_download_root, in_memory=True)

    def listen(self):
        stream = sd.Stream(channels=1, samplerate=16000)
        stream.start()
        data , overflowed = stream.read(1024)
        stream.stop()
        print(data)   
        audio = whisper.pad_or_trim(data)
        mel = whisper.log_mel_spectrogram(audio, n_mels=self.model.dims.n_mels).to(self.model.device)
        _, probs = self.model.detect_language(mel)
        options = whisper.DecodingOptions()
        result = whisper.decode(self.model, mel, options)
        print(result.text)

if __name__ == "__main__":
    stt = Stt()
    stt.listen()
    
    