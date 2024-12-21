# EUR-Lex-Triples: A Legal Relation Extraction Dataset from European Legislation
EUR-Lex-Sum dataset [Aumiller, 2022](https://aclanthology.org/2022.emnlp-main.519.pdf) annotated with triples

## Dataset Description
* EUR-Lex-Triples consists on 1504 annotated documents. All Documents come from the english part of EUR-Lex-Sum Dataset.
* [Dataset](Dataset) repository contains json files containing for each document its summary, the annotated paragraphs, and for each paragraph the triples derived from the annotations.

* Here is an example of a document of EUR-Lex-Sum with its associated triples : ![Here is an example of EUR-Lex-Triples](EUR-Lex-Triples-Examples.jpg)

* Number of occurrences of different entity and verb types across the dataset in documents (Docs) and summaries (Sums) : ![Here is an example of EUR-Lex-Triples](Entities-Verbs.jpg)


rep : Dataset
  - readme
  - fichiers txt par document
rep : code
 - readme
 - sous-rep : preprocessing
 - sous-rep : annotation tool
 - RE baseline : lancement des codes des baseline, résultats obtenus
Dublin-Core
## citation
EUR-Lex-Triples: A Legal Relation Extraction Dataset from European Legislation. Nihed Bendahman, Karen Pinel-Sauvagnat, Gilles Hubert and Mokhtar Boumedyen Billami. Paper submitted to ESWC 2025.
## Licence
Copyright for the editorial content of EUR-Lex website, the summaries of EU legislation and the consolidated texts owned by the EU, are licensed under the Creative Commons Attribution 4.0 International licence, i.e., CC BY 4.0 as mentioned on the official EUR-Lex website. Any data artifacts remain licensed under the CC BY 4.0 license.
