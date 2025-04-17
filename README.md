# EUR-Lex-Triples: A Legal Relation Extraction Dataset from European Legislation
EUR-Lex-Sum dataset [Aumiller, 2022](https://aclanthology.org/2022.emnlp-main.519.pdf) annotated with triples

## Dataset Description
* EUR-Lex-Triples consists on 1504 annotated documents. All Documents come from the english part of EUR-Lex-Sum Dataset.
* [Dataset](https://github.com/NihedB/EUR-Lex-Triples/tree/main/Dataset) contains json files containing for each document its summary, the annotated paragraphs, and for each paragraph the triples derived from the annotations.
  
## Installation
Install all necessary dependencies by running : 
``` python3 -m pip install -r requirements.txt ```

## Data Preprocessing
* [Code/Preprocessing](https://github.com/NihedB/EUR-Lex-Triples/tree/main/Code/Preprocessing) contains the code used for the pre-processing of documents for the annotation process.
  
## Annotation Tool
* [Code/Annotation-Tool](Code/Annotation-Tool) contains the code used for the annotation tool we developed as well as the detailed guidelines and some [examples](Code/Annotation-Tool/examples.pdf);
   
## Relation Extraction Baselines
* [Code/RE-Baselines](Code/RE-Baselines) contains the code used to run the RE baselines : Fine-Tuning and Inference.
* Results of baseline models for Relation Extraction are : 

|  Model                  |  Precision      |  Recall         |  F1-Score       |
|-----------------        |-----------------|-----------------|-----------------| 
| Legal-Bert              |                 |                 |                 |
| Bert                    |     0.58        |       0.52      |      0.54       |
| Rebel-Large             |     0.88        |       0.75      |      0.80       | 
| Mistral 7b zero-Shot    |    0.38         |       0.30      |     0.33        |
| Mistral 7b In-Context   |    0.42         |       0.36      |     0.38        |
| Mistral 7b Finetuning   |    0.84         |       0.69      |     0.75        |
| Zephyr 7b Zero-Shot     |     0.40        |      0.36       |      0.37       |
| Zephyr 7b In-Context    |     0.52        |        0.44     |        0.47     |
| Zephyr 7b Finetuning    |      0.85       |      0.61       |       0.71      |
| Llama 2 13b Zero-Shot   |       0.31      |       0.25      |      0.27       |
| Llama 2 13b In-Context  |        0.33     |       0.29      |     0.30        |
| Llama 2 13b Finetuning  |        0.82     |        0.61     |           0.69  |
## Citation
EUR-Lex-Triples: A Legal Relation Extraction Dataset from European Legislation. 
Paper submitted to TPDL 2025.
## Licence
Copyright for the editorial content of EUR-Lex website, the summaries of EU legislation and the consolidated texts owned by the EU, are licensed under the Creative Commons Attribution 4.0 International licence, i.e., CC BY 4.0 as mentioned on the official EUR-Lex website. Any data artifacts remain licensed under the CC BY 4.0 license.
