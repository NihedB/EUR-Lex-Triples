import json
import re
import os
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForCausalLM, DataCollatorForSeq2Seq, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)

train, valid, test = [], [], []

with open('train_with_annotations.json', "r", encoding="utf8") as f:
   train = json.load(f)

with open('validation_with_annotations.json', "r", encoding="utf8") as f:
    valid = json.load(f)

with open('test_rel_with_annotations.json', "r", encoding="utf8") as f:
    test = json.load(f)

train_data = []

not_annotated = 0
i=0
for element in train :
  try :
    samples, i = sampling_data(element, i)
    for key, value in samples.items() :
      doc ={}
      doc["text"] = value["text"]
      doc["triplets"] = value["triplets"]
      train_data.append(doc)
  except :
    not_annotated +=1

valid_data = []

not_annotated = 0
i=0
for element in valid :
  try :
    samples, i = sampling_data(element, i)
    for key, value in samples.items() :
      doc ={}
      doc["text"] = value["text"]
      doc["triplets"] = value["triplets"]
      valid_data.append(doc)
  except :
    not_annotated +=1



# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
model_name = "meta-llama/Llama-2-13b-chat-hf"
output_dir = "./llama_relation_extraction_finetuned"
max_source_length = 256
max_target_length = 128


# Création des datasets Hugging Face à partir de listes Python
train_dataset = Dataset.from_list(train_data)
valid_dataset = Dataset.from_list(valid_data)

# Création d'un DatasetDict
dataset = DatasetDict({
    "train": train_dataset,
    "validation": valid_dataset
})

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    load_in_4bit=True,
    device_map="auto"
)

#model.gradient_checkpointing_enable()
#model.enable_input_require_grads()
#model.is_parallelizable = True
#model.model_parallel = True

# Configurer LoRA
lora_config = LoraConfig(
    r=8,                         # rang des matrices LoRA
    lora_alpha=16,
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM # type de tâche
)

# Appliquer LoRA au modèle
model = get_peft_model(model, lora_config)


max_length = 256
def format_and_tokenize(example):
    # On concatène l'entrée et la cible en une seule séquence
    # Prompt
    input_text = "Extract the relation triplets from the following text:\n" + example["text"] + "\nTriplets:"
    # Cible (triplets) convertie en texte
    target_text = str(example["triplets"])

    # On crée une seule séquence contenant prompt + réponse
    full_text = input_text + " " + target_text

    # On tokenize la séquence complète
    tokens = tokenizer(full_text, truncation=True, max_length=max_length)

    # Les labels sont identiques aux input_ids dans le cadre d'un causal LM
    tokens["labels"] = tokens["input_ids"].copy()

    return tokens

dataset = dataset.map(format_and_tokenize, remove_columns=dataset["train"].column_names)

train_dataset = dataset["train"]
valid_dataset = dataset["validation"]

data_collator = DataCollatorForLanguageModeling(tokenizer, pad_to_multiple_of=8, mlm=False)

########################################################################
# Entraînement
########################################################################

training_args = TrainingArguments(
    output_dir=output_dir,
    overwrite_output_dir=True,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=4,
    evaluation_strategy="steps",
    eval_steps=500,
    save_steps=500,
    logging_steps=500,
    num_train_epochs=5,
    learning_rate=1e-4,
    bf16=False,  # Désactiver bf16 si vous rencontrez des problèmes, sinon True si GPU supporté
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=valid_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator
)

########################################################################
# Lancement de l'entraînement
########################################################################

trainer.train()

trainer.save_model("checkpoints/Llama_fn_5_epochs")