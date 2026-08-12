
#import whisper
from path import model_download_root
import sounddevice as sd
import openwakeword 
from openwakeword.model import Model
import pyaudio
import time
import threading


from faster_whisper import WhisperModel
import numpy as np




class Listener:
    def __init__(self):
        self.SAMPLE_RATE =  16000
        self.CHUNK_SIZE = 1280
        self.FORMAT = pyaudio.paInt16
        self.p = pyaudio.PyAudio()
        # self.stt = Stt()
        self.stream = self.p.open(format = self.FORMAT, channels= 1, rate = self.SAMPLE_RATE, input=True , output=True, frames_per_buffer=self.CHUNK_SIZE)

    def mic_data(self,queue):
        while True:
            raw_data = self.stream.read(self.CHUNK_SIZE)
            data = np.frombuffer(raw_data,dtype=np.int16)
            queue.append(data)
            # print(data)
            # print(type(data))
            # time.sleep(0.5)
            time.sleep(0.05)
            


class Stt():
    def __init__(self):
        self.is_running = True
        self.SAMPLE_RATE = 16000
        self.CHUNK_SIZE = 1280
        self.mic_queue = []

        # ----- openai-whisper ----- START
        #self.stt_model = whisper.load_model(name = "small", download_root=model_download_root, in_memory=True)
        
        
        # openwakeword.utils.download_models(target_directory=f"{model_download_root}/openwakeword_models")
        self.wakeword_model = Model(
            wakeword_models=[f"{model_download_root}/openwakeword_models/hey_jarvis_v0.1.onnx"],
            melspec_model_path=f"{model_download_root}/openwakeword_models/melspectrogram.onnx",
            embedding_model_path=f"{model_download_root}/openwakeword_models/embedding_model.onnx",
            inference_framework="onnx"
            )

        # ----- openai-whisper ----- END
        
        # ----- faster-whisper ----- START
        self.faster_whisper_model = WhisperModel("small",download_root= model_download_root,compute_type="int8")
        # ----- faster-whisper ----- END

    def wake_word(self,queue):
            print("Wake Word is Listening...")
            while True:
                if  queue:
                    data = queue.pop(0)
                    #print(data)  
                    self.prediction = self.wakeword_model.predict(data)
                    for wake_word , score in self.prediction.items():
                        if score >= 0.5:
                            print(wake_word, score)
                            return self.stt()
                        #else:
                            #print("failed: ",wake_word,float(score))
                            
                        
            
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
        
        


    def stt(self):
        
        #audio = self.get_audio(duration= 5)
        
        
        # #---- whisper START -----
        
        # audio = whisper.pad_or_trim(audio)
        # mel = whisper.log_mel_spectrogram(audio, n_mels=self.stt_model.dims.n_mels).to(self.stt_model.device)
        # _, probs = self.stt_model.detect_language(mel)
        # options = whisper.DecodingOptions()
        # result = whisper.decode(self.stt_model, mel, options)
        # print(result.text)
        
        # #---- whisper END -----


        # ---- faster-whisper START -----
        #print(mic_queue)
        #print(self.mic_queue)
        time.sleep(10)
        #print(self.mic_queue)
        #print(type(self.mic_queue))
        #print(np.ndarray(self.mic_queue).flatten())
        #self.mic_queue = self.mic_queue[0:10]
        #print(self.mic_queue)
        # self.mic_queue = self.mic_queue[0:][0]
        self.mic_queue = np.concatenate(self.mic_queue)
        #print(self.mic_queue)
        #time.sleep(1)
        #print("STT:",self.mic_queue)
        #segments , info = self.faster_whisper_model.transcribe(audio= mic_queue)
        segments , info = self.faster_whisper_model.transcribe(audio= self.mic_queue)
        for segment in segments:
            print("STT: ","[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

        # ---- faster-whisper END -----

        
        
        
        
        
        




    

if __name__ == "__main__":
    #mic_queue = []
    listener = Listener()
    stt = Stt()
    mic_queue = stt.mic_queue
    t1 = threading.Thread(target=listener.mic_data, args=(mic_queue,), daemon=True)
    t2 = threading.Thread(target=stt.wake_word, args=(mic_queue,), daemon=True)
    t1.start()
    t2.start()

    while True:
        time.sleep(0.05)
    

    