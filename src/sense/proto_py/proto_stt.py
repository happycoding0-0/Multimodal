

import wave
import pyaudio
import time
CHUNK  = 1024
RATE = 16000
p = pyaudio.PyAudio()
stream = p.open(rate=RATE,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=CHUNK)




d = []
try:
    print("recording...")
    while True:
        
        data= stream.read(num_frames=CHUNK)
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

from faster_whisper import WhisperModel

from sense.path import model_download_root

model = WhisperModel("small",device="cuda",download_root=model_download_root, compute_type="int8")

segments, info = model.transcribe("test.wav",vad_filter=True)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))





