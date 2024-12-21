import json
import re
import os
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForCausalLM, DataCollatorForSeq2Seq, Trainer, TrainingArguments
import nltk
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer

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
data_train["labels"] = []

not_annotated = 0
i=0
for element in train :
  try :
    samples, i = sampling_data(element, i)
    for key, value in samples.items() :
      #data_train["labels"] = []
      if len(value["triplets"]) == 1 :
        print("triplet :", value["triplets"][0][0])
        #data_train["labels"].append(value["triplets"][0][0])
        triplet = value['triplets'][0][0].replace("[ ", "").replace(" ]", "").split(",")
        #print("triplet:",triplet[1])
        #print("hello")
        data_train["text"].append(value["text"])
        if lemmatizer.lemmatize(triplet[1].lower().replace(" ", ""), pos="v")=="implement":
          print(triplet)
        data_train["labels"].append(triplet[1])
  except :
    not_annotated +=1


label_mapping_inv = {"repeal" : 0 , "amend":1, "supplement":2, "replace":3, "correct":4, "recast":5, "extend":6, "implement" : 7}

labels = []
for verb in data_train["labels"] :
  v = label_mapping_inv[lemmatizer.lemmatize(verb.lower().replace(" ", ""), pos="v")]
  print(v)
  labels.append(v)


label_mapping_inv = {"repeal" : 0 , "amend":1, "supplement":2, "replace":3, "correct":4, "recast":5, "extend":6, "implement" : 7}

labels = []
for verb in data_train["labels"] :
  v = label_mapping_inv[lemmatizer.lemmatize(verb.lower().replace(" ", ""), pos="v")]
  labels.append(v)

# 1. Dataset pour la classification des relations
class RelationExtractionDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        text = self.texts[index]
        label = self.labels[index]

        # Tokenizer le texte
        encoding = self.tokenizer(
            text,
            max_length=self.max_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),  # Tensor Long
            "attention_mask": encoding["attention_mask"].squeeze(0),  # Tensor Long
            "labels": torch.tensor(label, dtype=torch.long),  # Labels Long
        }

texts = data_train["text"]

print("taille textes : ", len(texts))
print("taille labels: ", len(labels))

# Label mapping (ajoutez d'autres relations ici)
label_mapping = {0: "repeal", 1: "amend", 2:"supplement", 3:"replace", 4:"correct", 5:"recast", 6:"extend", 7:"implement"}

# Charger le tokenizer
tokenizer = BertTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")

# Créer le dataset
dataset = RelationExtractionDataset(texts, labels, tokenizer)

# 3. Charger le modèle pré-entraîné
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=len(label_mapping),
)

# 4. Paramètres d'entraînement
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=5,
    per_device_train_batch_size=2,
    evaluation_strategy="no",
    save_strategy="no",
    logging_dir="./logs",
    logging_steps=100,
    learning_rate=5e-5,
)


# 5. Utiliser le Trainer pour entraîner
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
)

# Entraîner le modèle
trainer.train()

