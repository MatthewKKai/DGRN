import json
import pandas as pd
import numpy as np
import re
import csv
import nltk

corpus_path = r"../data/cancer_corpus.json"
triple_path = r"../data/sldb_complete_triple.csv"

def get_corpus(corpus_path):
    abstract_pair = {}
    with open(corpus_path, encoding = "utf-8") as f:
        data = json.load(f)
        i = 0
        for key0 in data.keys():
            temp = data[key0]
            for tmp_data in temp:
                try:
                    citing_abstract = re.search("p>.*</p", tmp_data["citing_abstract"]).group().strip("p>").strip("</p")
                    cited_abstract = re.search("p>.*</p", tmp_data["cited_abstract"]).group().strip("p>").strip("</p")
                    citing_abstract_words = []
                    cited_abstract_words = []
                    for word in nltk.sent_tokenize(citing_abstract):
                        citing_abstract_words.append(nltk.word_tokenize(word))
                    for word in nltk.sent_tokenize(cited_abstract):
                        cited_abstract_words.append(nltk.word_tokenize(word))
                    tmp_dict = {"citing_abstract":citing_abstract_words, "citied_abstract":cited_abstract_words}
                    abstract_pair[i] = tmp_dict
                    i += 1
                    # print("Citing_Abstract:{0}\n----\nCited_Abstract:{1}\n****\n".format(citing_abstract,cited_abstract))
                except Exception as e:
                    pass
    return abstract_pair

def triple_annotator(triple_path, corpus):
    triple_data = pd.read_csv(triple_path, encoding="utf-8")
    annotated_data = {}
    for key in corpus.keys():
        tmp_citing = corpus[key]["citing_abstract"]
        tmp_cited = corpus[key]["citied_abstract"]
        tmp_citing_annotated = tmp_citing
        tmp_cited_annotated = tmp_cited
        for i in range(len(triple_data)):
            if triple_data["head_name"][i] in tmp_citing and triple_data["tail_name"][i] in tmp_citing:
                tmp_citing_annotated = tmp_citing_annotated + "\n" + triple_data["head_name"][i] + "," + triple_data["edge_type"][
                    i] + "," + triple_data["tail_name"][i]
                print(tmp_citing_annotated)
            if triple_data["head_name"][i] in tmp_cited and triple_data["tail_name"][i] in tmp_cited:
                tmp_cited_annotated = tmp_cited_annotated + "\n" + triple_data["head_name"][i] + "," + triple_data["edge_type"][
                    i] + "," + triple_data["tail_name"][i]
        annotated_data[key] = {"citing_data":tmp_citing_annotated, "cited_data":tmp_cited_annotated}
    return annotated_data

abstract_pair = get_corpus(corpus_path)
annotated_data = triple_annotator(triple_path, abstract_pair)

with open("../data/annotated_data.csv", "w") as f:
    writer = csv.writer(f)
    for key, value in annotated_data.items():
        writer.writerow([key, value])

print(len(abstract_pair))
print(len(annotated_data))