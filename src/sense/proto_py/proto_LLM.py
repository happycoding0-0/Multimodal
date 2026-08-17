import os
import torch
import transformers
from sense.path import llama_3_8B, llama_3_8B_config
from sense.proto_py.proto_tts import tts  

# Force offline mode to prevent any hidden internet requests
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

model_id = llama_3_8B  # This is the path to your model directory

# 1. Load the model and tokenizer directly first (Safest for complex models like Llama 3)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_id, 
    local_files_only=True
)

model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    config=llama_3_8B_config,         # Pass your specific sense config here
    torch_dtype=torch.bfloat16,       # Best precision for Llama 3
    local_files_only=True
)

# 2. Pass the instantiated objects into the pipeline
pipeline = transformers.pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0
)

# 3. Run generation with required Llama 3 parameters
response = pipeline(
    "Hey do you know jarvis?", 
    max_new_tokens=50,
    pad_token_id=tokenizer.eos_token_id  # Llama 3 requires explicit pad token setting
)

print(response)
text= response[0]["generated_text"]
print(text)
tts(text)
