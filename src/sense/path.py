import json
from pathlib import Path

SENSE_DIR = Path(__file__).resolve().parent


path_json = str(SENSE_DIR / "models/path.json")

with open(path_json, "r", encoding="utf-8") as f:
    path_ = json.load(f)
    # print(path_)


# path : vision model 
yolo_model = str(SENSE_DIR / path_["yolo_model"]) 

# path : speech model(tts, text to speech)
kokoro_model = str(SENSE_DIR / path_["kokoro_model"])
kokoro_config = str(SENSE_DIR / path_["kokoro_config"])
#kokoro_voice_model = str(SENSE_DIR / path_["kokoro_voice_model"])
bm_fable = str(SENSE_DIR/path_["kokoro_voice_model"]["bm_fable"])
bm_daniel = str(SENSE_DIR/path_["kokoro_voice_model"]["bm_daniel"])
bm_george = str(SENSE_DIR/path_["kokoro_voice_model"]["bm_george"])
bm_lewis = str(SENSE_DIR/path_["kokoro_voice_model"]["bm_lewis"])
bf_alice = str(SENSE_DIR/path_["kokoro_voice_model"]["bf_alice"])
bf_emma = str(SENSE_DIR/path_["kokoro_voice_model"]["bf_emma"])
af_heart = str(SENSE_DIR/path_["kokoro_voice_model"]["af_heart"])
