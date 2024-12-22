import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


output_dir = "checkpoints/model_checkpoint"


tokenizer = AutoTokenizer.from_pretrained(output_dir, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    output_dir,
    trust_remote_code=True,
    device_map="auto"
)

input_text = (
    "Extract the relational triples from the following text:\n"
    "Commission Delegated Regulation (EU) 2019/980 of 14 March 2019 supplementing Regulation (EU) 2017/1129."
    "Triplets:"
)

inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

with torch.no_grad():
    output_ids = model.generate(
        **inputs,
        max_new_tokens=80,
        temperature=0.1,     # Ajuster la température pour plus ou moins de diversité
        do_sample=False,      # Autoriser l'échantillonnage pour plus de diversité
        top_p=0.2,           # Nucleus sampling
        pad_token_id=tokenizer.eos_token_id
    )


response = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("Generated answer :", response)