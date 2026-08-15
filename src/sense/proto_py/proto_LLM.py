from transformers import pipeline
from sense.path import Qwen_dir
pipe = pipeline("text-generation",model="Qwen/Qwen3-0.6B",device_map="auto",model_kwargs={"cache_dir":Qwen_dir})

messages = [
    {"role": "user", "content": "자비스 너는 누구지?"},
]
outputs = pipe(messages)
print(outputs[0]["generated_text"][-1]["content"])