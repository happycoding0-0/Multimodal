

import wave
import pyaudio
import time

from faster_whisper import WhisperModel

from sense.path import model_download_root
import threading 
import queue



MODEL = "small"
model = WhisperModel(MODEL,download_root=model_download_root,compute_type="int8")


CHUNK  = 1024
RATE = 16000
p = pyaudio.PyAudio()
stream = p.open(rate=RATE,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=CHUNK)
q = queue.Queue(maxsize=30)



def mic(q):
    while True:
        data= stream.read(num_frames=CHUNK)
        q.put(data)

def record(q):
    
    d = []
    try:
        print("recording...")
        while True:
            data = q
            d.append(data)
            
    except KeyboardInterrupt:
        print("done")
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()

    file = wave.open("test.wav","wb")
    file.setnchannels(1)
    file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    file.setframerate(RATE)
    file.writeframes(b''.join(d))

    file.close()

def stt():
    

    segments, info = model.transcribe("test.wav",vad_filter=True)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))





if __name__ == "__main__":
    t_mic = threading.Thread(target= mic, args=(q,),daemon=True)
    t_rec = threading.Thread(target= record, args=(q,),daemon=True)

    t_mic.start()
    t_rec.start()

    while True:
        print("end")
        time.sleep(1)