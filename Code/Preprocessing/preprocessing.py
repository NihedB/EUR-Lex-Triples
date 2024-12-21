from bs4 import BeautifulSoup
import json
import re
import inflect
import os
import shutil


english_corpus = []

with open('Data/EUR-Lex-Sum/train_preprocessed.json', "r", encoding="utf8") as f:
   english_corpus = json.load(f)

with open('Data/EUR-Lex-Sum/validation_preprocessed.json', "r", encoding="utf8") as f:
    english_corpus.extend(json.load(f))

with open('Data/EUR-Lex-Sum/test_preprocessed.json', "r", encoding="utf8") as f:
    english_corpus.extend(json.load(f))

print(len(english_corpus))


def extract_lawentities (text) :
    #print("text recu")
    p = inflect.engine()
    types = ["directives", "regulations", "decisions", "articles", "decisions", "directive", "regulation", "decision", "resolution", "recommendations", "recommendation", "opinions", "opinion", "resolutions"]
    regex = {
        
        "lawentity" : r"(\b(\b(directives|regulations|decisions|directive|regulation|decision|opinions|opinion|recommandations|recommandation|resolution|resolutions|position|positions)+\s*(\(\w{0,3}|\w{0,7}\))*(\(\w{0,3}, \w{0,7}\))*\s*((n|no|num|numero)(°)?)?\s*((\d)+(/|-)+(\d)+(/|-)*(\w{2,5})*)+)\b)",
        "lawentity_ann" : r"(\b(\b(directives|regulations|decisions|directive|regulation|decision|opinions|opinion|recommandations|recommandation|resolution|resolutions|position|positions)+\s*(\(\w{0,3}|\w{0,7}\))*(\(\w{0,3}, \w{0,7}\))*\s*((n|no|num|numero)(°)?)?\s*((\d)+(/|-)+(\d)+(/|-)*(\w{2,5})*)+)((\s*(\,|and)\s*)\s*(\(\w{0,3}|\w{0,7}\))*(\(\w{0,3}, \w{0,7}\))*\s*((n|no|num|numero)(°)?)?\s*((\d)+(/|-)+(\d)+(/|-)*(\w{2,5})*)+\b)*)"
        }
    entities = []    
    for r in regex.keys() : 
        p2 = re.compile(regex[r], re.IGNORECASE)
        m2 = p2.findall(text)
        for pattern in m2 : 
            new_ent = ""
            if r=="lawentity_ann" :
                ents = pattern[0].replace(" and",",").split(",")
                type_ = ents[0].split(" ")[0]
                singular = p.singular_noun(type_)
                if singular :
                    type_=singular
                try : 
                    code_ = ents[0].split(" ")[len(ents[0].split())-1]
                    new_ent = new_ent + type_.lower()+" "+code_.lower().replace("-","/")
                    entities.append(type_.lower()+" "+code_.lower().replace("-","/"))
                    concat = ents[0].split(" ")
                    for t in concat :
                        if t.lower() in types : 
                            type_ = t
                            singular = p.singular_noun(type_)
                            if singular :
                                type_=singular     
                
                    for i in range(1,len(ents)):
                        new_ent = new_ent + " " + type_.lower()+" "+ ents[i].split(" ")[len(ents[i].split(" "))-1].lower().replace("-","/")
                        entities.append(type_.lower()+" "+ ents[i].split(" ")[len(ents[i].split(" "))-1].lower().replace("-","/"))
                except :
                    print("entité problématique : ", ents)
            else : 
                
                type_ = pattern[0].split(" ")[0]
                singular = p.singular_noun(type_)
                if singular :
                    type_=singular
                code_ = pattern[0].split(" ")[len(pattern[0].split(" "))-1]
                new_ent = type_.lower()+" "+code_.lower().replace("-","/")
                entities.append(new_ent)
                #entities.append(pattern[0])
                #replace entities in the texte : 
                #print(text," ////////////////////////// ",pattern[0])
            try :
                text = text.replace(pattern[0], new_ent)
            except :
                print("doc problématique : ", pattern[0], " ---> ", new_ent)
    return entities, text

def extract_verbs(text) :
    relations = ["amending", "supplementing", "repealing", "replacing", "correcting", "implementing", "recasting","extending", "amends", "supplements", "repeals", "replaces", "corrects", "implements", "amended", "supplemented", "repealed", "replaced", "corrected", "implemented", "extends", "recasts", "extended", "recasted"]
    found_verbs = []
    
    for r in relations : 
        if r in text.lower() : 
            found_verbs.append(r)
    return found_verbs

def display_paragraph(text) : 
    paragraphs = text.split("\n")
    displayed_paragraphs = []
    new_paragraphs = []
    new_paragraphs.append(paragraphs[0])
   
    index = 1
    if len(paragraphs)> 0 :
        for i in range(1, len(paragraphs)) : 
            if len(paragraphs[i])!=0 :
                if paragraphs[i][0].islower() : 
                    new_paragraphs[index-1] =  new_paragraphs[index-1] + "---" + paragraphs[i]
                else :
                    new_paragraphs.append(paragraphs[i])
                    index += 1

    i=0

    for p in new_paragraphs : 
        found_verbs = extract_verbs(p)
        found_entities = extract_lawentities(p)
    
        if len(found_verbs) > 0 and len(set(found_entities[0])) > 1 : 
            displayed_paragraphs.append(found_entities[1])
        i+=1
    return displayed_paragraphs


def modifyRoot_paquet(input_file, output_file, corpus) : 
    with open(input_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Trouver la liste des documents
    document_list = soup.find('ul', id='documentList')

    document_list.clear()
    for doc in corpus:
        li_tag = soup.new_tag('li')
        if doc[1].startswith("sum") : 
            name = "documents/sum_" + doc[0] + ".html"
            a_tag = soup.new_tag('a', href=name, **{'data-id':"sum_"+doc[0]})
            a_tag.string = "Summary"+doc[0]
            li_tag.append(a_tag)
            document_list.append(li_tag)
        else : 
            name = "documents/doc_" + doc[0] + ".html"
            a_tag = soup.new_tag('a', href=name, **{'data-id':"doc_"+doc[0]})
            a_tag.string = "Document "+doc[0]
            li_tag.append(a_tag)
            document_list.append(li_tag)
        
        
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup.prettify()))


def modify_html_paquet(input_file, output_file, new_items, reference, verbs, id, next_doc, summary=False):
    # Ouvrir et lire le fichier HTML d'entrée
    with open(input_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')

    # Trouver la balise <p> avec l'id "text" et modifier son contenu
    div_tag = soup.find('div', id='carouselContent')
    paragraphs =  display_paragraph(reference)
    new_content = ''.join(f'{paragraph}</br>' for paragraph in paragraphs).rstrip('</br>')
    #print("new_content : ", new_content)
    if div_tag:
        #print("file done")
        div_tag.clear()  # Efface le contenu existant
        for element in paragraphs:
            p_tag = soup.new_tag('p')
            p_tag.string = element
            div_tag.append(p_tag)
        #p_tag.append(BeautifulSoup(new_content, 'lxml'))
    
    if next_doc != None :
        next_id_tag = soup.find('input', id='nextDocumentUrl')
        next_id_tag.clear()
        if summary :
            next_id_tag["value"] = "doc_" + next_doc + ".html"
        else :
           next_id_tag["value"] = "sum_" + next_doc + ".html" 
     
    id_tag = soup.find('input', id='documentId')
    id_tag.clear()
    if summary :
        id_tag["value"] = "sum_"+id
    else :
        id_tag["value"] = "doc_"+id

    link = "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A"+str(id)+"&qid=1726477566260"
    href_tag = soup.find('a', id="doc_traduction")
    #href_tag.clear()
    href_tag["href"] = link

    #print(id, "  --- ", link)
    
    input_tag = soup.find('input', id='entitiesList')
    if not input_tag:
        print(f"No <ul> tag with id 'entityList' found in {input_file}.")
        return

    input_tag.clear()
    new_items = list(new_items)
    if len(new_items)> 0 : 
        input_tag['value'] = new_items[0]
        for i in range(1, len(new_items)) : 
            input_tag['value'] = input_tag['value'] + "," + new_items[i]

    verb_tag = soup.find('input', id='verbList')
    if not verb_tag:
        print(f"No <ul> tag with id 'verbList' found in {input_file}.")
        return

    verb_tag.clear()
    verbs = list(verbs)
    if len(verbs)> 0 : 
        verb_tag['value'] = verbs[0]
        for i in range(1, len(verbs)) : 
            verb_tag['value'] = verb_tag['value'] + "," + verbs[i]

    # Écrire le nouveau contenu dans le fichier de sortie
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def create_docs_paquet(input_file, input_file_last, output_folder, paquet) :
    i=0
    while i in range(0, len(paquet)) :
        #print(paquet[i][1], paquet[i][0])
        if paquet[i][1].startswith("sum") :
            output_file = output_folder +"sum_" + paquet[i][0]+".html"  
            entities, reference =  extract_lawentities(paquet[i][2])
            #print("id -- ", paquet[i][0])
            verbs = extract_verbs(paquet[i][2])
            summary=True
        else :
            output_file = output_folder +"doc_" + paquet[i][0]+".html"
            entities, reference =  extract_lawentities(paquet[i][2])
            #print("premier appel -- ")
            verbs = extract_verbs(paquet[i][2])
            summary=False
        if i <= len(paquet) - 2 :
            #print("appel depassé ")
            modify_html_paquet(input_file, output_file,set(entities), paquet[i][2], verbs, paquet[i][0], paquet[i+1][0], summary)
        else : 
            #print("appel depassé ")
            modify_html_paquet(input_file_last, output_file,set(entities), paquet[i][2], verbs, paquet[i][0], None, summary)
        i+=1  
        
def paquet_to_rep(paquets) : 
    i=0
    for paquet in paquets :
        types = [e[1] for e in paquet]
        if "sum_acc" in types :
            dir_name = f"paquet_annotation_{i}_acc"
        else :
            dir_name = f"paquet_annotation_{i}"
        
        dir_path = os.path.join("Annotation/paquets", dir_name)
        os.makedirs(dir_path, exist_ok=True)
        name_folder = "Annotation/paquets/" + dir_name
        modifyRoot_paquet("Annotation/annotation.html", name_folder + "/annotation.html", paquet)

        input_file = 'Annotation/documents/doc_1.html'  
        input_file_last = 'Annotation/documents/doc_last.html'  

        
        sub_dir_name = "documents"
        sub_dir_path = os.path.join(name_folder, sub_dir_name)
        os.makedirs(sub_dir_path, exist_ok=True)

        create_docs_paquet(input_file, input_file_last, name_folder+"/documents/", paquet)
        
        shutil.copy("Annotation/filesystem.js", name_folder +"/filesystem.js")
        shutil.copy("Annotation/script.js", name_folder +"/script.js")
        shutil.copy("Annotation/styles.css", name_folder +"/styles.css")
        shutil.copy("Annotation/examples.pdf", name_folder +"/examples.pdf")
        
        i+=1