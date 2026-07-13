from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM
import torch

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto"
)


def get_response(user_message, sentiment):

    if sentiment == "Positive":
        system_prompt = (
            "You are a cheerful and friendly AI assistant. "
            "Respond positively and encourage the user."
        )

    elif sentiment == "Negative":
        system_prompt = (
            "You are an empathetic AI assistant. "
            "Comfort the user and provide supportive responses."
        )

    else:
        system_prompt = (
            "You are a professional AI assistant. "
            "Answer clearly and directly."
        )

    prompt = f"""
<|system|>
{system_prompt}

<|user|>
{user_message}

<|assistant|>
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=40,
        temperature=0.7,
        do_sample=True
    )

    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    if "<|assistant|>" in response:
        response = response.split("<|assistant|>")[-1]

    return response.strip()