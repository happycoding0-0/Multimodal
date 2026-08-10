
import whisper
from path import model_download_root
import sounddevice as sd
import openwakeword 
from openwakeword.model import Model
import pyaudio
import time
import threading


class Listener:
    def __init__(self, SAMPLE_RATE = 16000):
        self.SAMPLE_RATE = SAMPLE_RATE
        self.CHUNK_SIZE = 1280
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = pyaudio.paInt16, channels= 1, rate = self.SAMPLE_RATE, input=True , output=True, frames_per_buffer=self.CHUNK_SIZE)

    def listen(self,queue):
        while True:
            data = self.stream.read(self.CHUNK_SIZE, exception_on_overflow=False)
            queue.append(data)
            time.sleep(0.01)

    def run(self, queue):
        thread = threading.Thread(target= self.listen, args=(queue,),daemon=True)
        thread.start()
        print("Speech Recognition is now listening... \n")

class Stt():
    def __init__(self):
        self.SAMPLE_RATE = 16000
        self.CHUNK_SIZE = 1280
        self.stt_model = whisper.load_model(name = "small", download_root=model_download_root, in_memory=True)
        
        #openwakeword.utils.download_models(target_directory=f"{model_download_root}/openwakeword_models")
        self.wakeword_model = Model(
            wakeword_models=[f"{model_download_root}/openwakeword_models/hey_jarvis_v0.1.onnx"],
            melspec_model_path=f"{model_download_root}/openwakeword_models/melspectrogram.onnx",
            embedding_model_path=f"{model_download_root}/openwakeword_models/embedding_model.onnx",
            inference_framework="onnx"
            )

        self.listener = Listener(SAMPLE_RATE=16000)
        self.audio_q = list()
        

    def wake_word(self):
        pass
        # 구버전
        # with sd.InputStream(samplerate=self.SAMPLE_RATE , channels= 1, dtype='int16') as stream:
        #     print("Listening...")
        #     while True:
        #         audio_chunk, _ = stream.read(self.CHUNK_SIZE)
        #         audio_chunk =audio_chunk.flatten()
        #         self.prediction = self.wakeword_model.predict(audio_chunk)

        #         for wake_word, score in self.prediction.items():

        #             if score >=0.5:
        #                 print(wake_word, score)
                        
        #                 #return self.stt()
        #                 return  self.lisenter
        
        
    # def get_audio(self,duration = 5):
    #     print("recording...")
    #     self.audio = sd.rec(
    #         int(duration* self.SAMPLE_RATE),
    #         samplerate=self.SAMPLE_RATE,
    #         channels=1,
    #         dtype="float32"
    #                         )
    #     sd.wait()
    #     print("end recording")
    #     return self.audio.flatten()

    def stt(self):
        #audio = self.get_audio(duration= 5)
        
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio, n_mels=self.stt_model.dims.n_mels).to(self.stt_model.device)
        _, probs = self.stt_model.detect_language(mel)
        options = whisper.DecodingOptions()
        result = whisper.decode(self.stt_model, mel, options)
        print(result.text)

    def inference_loop(self):
        while True:
            if len(self.audio_q) < 5:
                continue
            else:
                self.pred_q = self.audio_q.copy()
                self.audio_q.clear()
                
                
            time.sleep(0.05)

    def run(self):
        self.listener.run(self.audio_q)
        thread = threading.Thread(target=self.inference_loop,
                                    # args=(action,)
                                    daemon=True)
        
        thread.start()
        while True:
            time.sleep(1)
            print(self.audio_q)

    

if __name__ == "__main__":
    stt = Stt()
    stt.run()
    # threading.Event().wait()
    #stt.wake_word()
    #print(f"{model_download_root}/openwakeword_models/hey_jarvis_v0.1.onnx")

    
    