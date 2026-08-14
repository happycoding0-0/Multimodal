
import sys
import os

# 현재 파일의 상위 폴더 경로를 구해서 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import onnxruntime as ort
from path import jarvis_model,jarvis_json
import json

# sess = ort.InferenceSession(jarvis_model)

# print("=== 입력 (모델이 뭘 받아먹나) ===")
# for inp in sess.get_inputs():
#     print(f"이름: {inp.name}, shape: {inp.shape}, 타입: {inp.type}")

# print("\n=== 출력 (모델이 뭘 뱉어내나) ===")
# for out in sess.get_outputs():
#     print(f"이름: {out.name}, shape: {out.shape}, 타입: {out.type}")



with open(jarvis_json,"r",encoding="utf-8") as f:
    jarvis_json_ = json.load(f)

phoneme_id_map = jarvis_json_["phoneme_id_map"]
noise_scale = jarvis_json_["inference"]["noise_scale"]
length_scale = jarvis_json_["inference"]["length_scale"]
noise_w = jarvis_json_["inference"]["noise_w"]
print(f"noise_scale : {noise_scale} ,length_scale : {length_scale}, noise_w: {noise_w}")

print(phoneme_id_map)