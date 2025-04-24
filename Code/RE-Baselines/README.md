This repository contains the baselines code used for the relation extraction task: 
* We tested 3 Pretrained Language Models (PLM): Legal Bert, Bert and REBEL-Large, and 3 Large Langage Models (LLM): Mistral-7b, Zephyr-7b, Llama-2-13b. All models were finetuned, the finetuning and inference code can be found in this repository.
* Additionally, we evaluated the LLMs using two other settings: Zero-shot semi-open RE prompting and In-Context learning. Prompts associated with these settings are in [Prompts](Prompts.txt).
* ```Checkpoints``` contains the checkpoints of the fine-tuned LLMs.
