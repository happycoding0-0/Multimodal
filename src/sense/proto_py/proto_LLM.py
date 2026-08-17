

# from transformers import pipeline
# from sense.path import Qwen_dir

# pipe = pipeline(
#     "text-generation",
#     model="Qwen/Qwen3-0.6B",
#     device_map="auto",
#     model_kwargs={"cache_dir": Qwen_dir},
    
# )

# # 프롬프트를 더 강력하고 명확하게 수정했습니다.
# messages = [
#     {
#         "role": "system",
#         "content": "You are JARVIS, the AI assistant from the movie Iron Man (2008). Always reply in JARVIS's professional, polite, and loyal tone. Do not break character.",
#     },
#     {"role": "user", "content": "hey jarvis daddy s home!"},
# ]

# # max_new_tokens를 지정하여 결과 길이를 확보합니다.
# outputs = pipe(messages, max_new_tokens=256)

# # 1. 생성된 전체 텍스트 가져오기
# raw_text = outputs[0]["generated_text"][-1]["content"]

# # 2. <think> 태그가 있다면 제거하고 실제 답변만 추출하기
# if "</think>" in raw_text:
#     final_reply = raw_text.split("</think>")[-1].strip()
# else:
#     final_reply = raw_text.strip()

# # 최종 자비스의 답변만 출력
# print(final_reply)

"""
ValueError: Couldn't instantiate the backend tokenizer from one of: 
(1) a `tokenizers` library serialization file, 
(2) a slow tokenizer instance to convert or 
(3) an equivalent slow tokenizer class to instantiate and convert. 
You need to have sentencepiece or tiktoken installed to convert a slow tokenizer to a fast one.

"""

from transformers import AutoModelForCausalLM, AutoTokenizer
from sense.path import Qwen_dir
model_name = Qwen_dir 

# load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name,local_files_only  =True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",local_files_only  =True
)

# prepare the model input
prompt = "what is jarvis?"
messages = [
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False # Switches between thinking and non-thinking modes. Default is True.
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

# conduct text completion
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=32768
)
output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

# parsing thinking content
try:
    # rindex finding 151668 (</think>)
    index = len(output_ids) - output_ids[::-1].index(151668)
except ValueError:
    index = 0

thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

print("thinking content:", thinking_content)
print("content:", content)
