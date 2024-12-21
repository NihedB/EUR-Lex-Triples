import json
import re
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from datasets import Dataset
from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, T5TokenizerFast, AutoModel, AutoModelForCausalLM
from transformers import DataCollatorForSeq2Seq, Trainer, TrainingArguments



lemmatizer = WordNetLemmatizer()


train, valid, test = [], [], []

with open('train_with_annotations.json', "r", encoding="utf8") as f:
   train = json.load(f)

with open('validation_with_annotations.json', "r", encoding="utf8") as f:
    valid = json.load(f)

with open('test_rel_with_annotations.json', "r", encoding="utf8") as f:
    test = json.load(f)


data_train = {}
data_train["text"] = []
data_train["relations"] = []

not_annotated = 0
i=0
for element in train :
  try :
    samples, i = sampling_data(element, i)
    for key, value in samples.items() :
      data_train["text"].append(value["text"])
      data_train["relations"].append(value["triplets"])
  except :
    not_annotated +=1

data_valid = {}
data_valid["text"] = []
data_valid["relations"] = []
i=0
for element in valid :
    samples, i = sampling_data(element, i)
    for value in samples.values() :
        print(len(value["triplets"]))
        data_valid["text"].append(value["text"])
        data_valid["relations"].append(value["triplets"])

dataset = Dataset.from_dict(data_train)
eval_dataset = Dataset.from_dict(data_valid)

def preprocess_function(examples):
    # Tokenize the input texts
    tokens = tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=512
    )

    # Create the target sequence for the relation extraction task
    labels = []
    for relations in examples["relations"]:
        #print("relations : ",relations)
        relation_text = ""
        for relation in relations :
          #print("relation : ",relation[0])
          triplet = relation[0].replace("[ ", "").replace(" ]", "").split(",")
          relation_text = relation_text + " " + triplet[0] + " " + triplet[1] + " " + triplet[2] + " |"

        print(relation_text)
        # Tokenize the relation text and add it as a label
        label_tokens = tokenizer(relation_text, padding="max_length", truncation=True, max_length=512).input_ids

        # Replace padding token id with -100 to ignore padding tokens in loss calculation
        label_tokens = [token if token != tokenizer.pad_token_id else -100 for token in label_tokens]

        labels.append(label_tokens)

    tokens['labels'] = labels
    return tokens



# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")


#tokenizer = AutoTokenizer.from_pretrained("lorahub/flan_t5_large-wiki_hop_original_explain_relation")
#model = AutoModelForSeq2SeqLM.from_pretrained("lorahub/flan_t5_large-wiki_hop_original_explain_relation")
#model.enable_input_require_grads() # only for the flan t5 model, not for rebel large.
gen_kwargs = {
    "max_length": 256,
    "length_penalty": 0,
    "num_beams": 3,
    "num_return_sequences": 3,
}

# Text to extract triplets from
text = 'Punta Cana is a resort town in the municipality of Higüey, in La Altagracia Province, the easternmost province of the Dominican Republic.'

# Tokenizer text
model_inputs = tokenizer(text, max_length=256, padding=True, truncation=True, return_tensors = 'pt')

# Generate
generated_tokens = model.generate(
    model_inputs["input_ids"].to(model.device),
    attention_mask=model_inputs["attention_mask"].to(model.device),
    **gen_kwargs,
)
# Apply the preprocessing function to the dataset
tokenized_dataset = dataset.map(preprocess_function, batched=True)
tokenized_eval_dataset = eval_dataset.map(preprocess_function, batched=True)


data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="no",  # <- No evaluation during training
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=6,
    weight_decay=0.01,
    save_total_limit=2,
    save_steps=10_000,
    warmup_steps=500,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_eval_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator
)

# Start training
trainer.train()

trainer.save_model("checkpoints/REBEL_Train")
