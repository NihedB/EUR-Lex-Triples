import nltk
import json
from nltk.stem import WordNetLemmatizer

"""
the program loads a json file, takes an annotation ("reference_annotation" or "summary annotation") and translates it into french triples.
"""

lemmatizer = WordNetLemmatizer()

file_path = "EUR-Lex-Triples/Dataset/Filtered_Annotated_Documents/document_21981A0905(01).json"  

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f) 

def mapping_triples (annotation) : 
    entities = {"directive" : "directive", "regulation" : "règlement", "decision" : "décision", "resolution" : "résolution", "recommandation" : "recommandation", "opinion" : "opinion"}

    verbs = {"amend" : "modifier", "supplement" : "compléter", "repeal" : "abroger", "replace" : "remplacer", "correct" : "corriger", "implement" : "mis en oeuvre" , "recast" : "refondre", "extend" : "étendre"}
    translated_triples = []
    for element in annotation.values() : 
        triples = element["triples"]
        print(triples)
        for triple in triples : 
            segments = triple.split(",")
            entity1 = segments[0]
            entity1 = entity1.replace(segments[0].lstrip().split(" ")[0], entities[segments[0].lstrip().split(" ")[0]])
            verb = segments[1]
            verb = verb.replace(segments[1].lstrip(), verbs[lemmatizer.lemmatize(segments[1].lstrip().lower(), pos="v")])
            entity2 = segments[2]
            entity2 = entity2.replace(segments[2].lstrip().split(" ")[0], entities[segments[2].lstrip().split(" ")[0]])
            translated_triple = [entity1, verb, entity2]
            translated_triples.append(translated_triple)
    return translated_triples

print("Translated annotated triples : ", mapping_triples (data["summary_annotations"]))