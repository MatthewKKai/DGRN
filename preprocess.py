import json
import pandas as pd
import numpy as np
import re
import os
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tqdm import tqdm
import pubmed_parser as pp

root_dir = r"data"
triple_path = r"data/sldb_complete_triple.csv"

def get_triple(triple_path):
    # entity length too long for processing, drop the relation between these entities
    drop_rel_list = ["PARTICIPATES_CpD", "PARTICIPATES_GpBP", "PARTICIPATES_GpCC", "PARTICIPATES_GpMF",
                     "PARTICIPATES_GpPW", "CAUSES_CcSE", "PRESENTS_DpS"]
    triple_data = pd.read_csv(triple_path, encoding="utf-8", error_bad_lines=False)
    for drop_item in drop_rel_list:
        triple_data = triple_data.drop(triple_data[triple_data["edge_type"] == drop_item].index)
    triple_data = triple_data.reset_index().drop("index", axis=1)
    return triple_data

def get_paper_info(corpus_path):
    # abstract_pair = {}
    # with open(corpus_path, encoding = "utf-8") as f:
    #     data = json.load(f)
    #     i = 0
    #     for key0 in data.keys():
    #         temp = data[key0]
    #         for tmp_data in temp:
    #             try:
    #                 citing_abstract = re.search("p>.*</p", tmp_data["citing_abstract"]).group().strip("p>").strip("</p")
    #                 cited_abstract = re.search("p>.*</p", tmp_data["cited_abstract"]).group().strip("p>").strip("</p")
    #                 citing_abstract_words = []
    #                 cited_abstract_words = []
    #                 for word in nltk.sent_tokenize(citing_abstract):
    #                     citing_abstract_words.append(nltk.word_tokenize(word))
    #                 for word in nltk.sent_tokenize(cited_abstract):
    #                     cited_abstract_words.append(nltk.word_tokenize(word))
    #                 tmp_dict = {"citing_abstract":citing_abstract_words, "citied_abstract":cited_abstract_words}
    #                 abstract_pair[i] = tmp_dict
    #                 i += 1
    #                 # print("Citing_Abstract:{0}\n----\nCited_Abstract:{1}\n****\n".format(citing_abstract,cited_abstract))
    #             except Exception as e:
    #                 pass
    abstract = get_abstract(corpus_path)
    intro = get_intro(corpus_path)
    citances = get_citances(corpus_path)
    paper = {"abstract": abstract,
                     "intro": intro,
                     "citances": citances}

    return paper


def get_intro(corpus_path):
    intro = []
    for item in pp.parse_pubmed_paragraph(corpus_path):
        if item["section"] == "Introduction":
            intro.append(item["text"])
    return ".".join(intro)    #list type


def get_abstract(corpus_path):
    return pp.parse_pubmed_xml(corpus_path)["abstract"]    # str type

def get_citances(corpus_path):
    text = []
    citances = []
    for item in pp.parse_pubmed_paragraph(corpus_path):
        text.append(item["text"])
    text = ".".join(text)
    sentence_ls = text.split(".")
    for item in sentence_ls:
        if "et al" in item and len(item)>40:
            citances.append(item)
    return ".".join(citances)  # list type

def paper_tokenizer(paper_info):
    try:
        stop_words = set(stopwords.words("english"))
        tokenized_paper = word_tokenize(paper_info)
    except Exception as e:
        print(e)
        nltk.download()
    paper_tokens = []
    for token in tokenized_paper:
        if token not in stop_words:
            paper_tokens.append(token.lower())
    return paper_tokens  # list type

def triple_annotator(triple_data, paper):
    # triple_data = pd.read_csv(triple_path, encoding="utf-8")
    # annotated_data = {}
    # for key in corpus.keys():
    #     tmp_citing = corpus[key]["citing_abstract"]
    #     tmp_cited = corpus[key]["citied_abstract"]
    #     tmp_citing_annotated = tmp_citing
    #     tmp_cited_annotated = tmp_cited
    #     for i in range(len(triple_data)):
    #         if triple_data["head_name"][i] in tmp_citing and triple_data["tail_name"][i] in tmp_citing:
    #             tmp_citing_annotated = tmp_citing_annotated + "\n" + triple_data["head_name"][i] + "," + triple_data["edge_type"][
    #                 i] + "," + triple_data["tail_name"][i]
    #             print(tmp_citing_annotated)
    #         if triple_data["head_name"][i] in tmp_cited and triple_data["tail_name"][i] in tmp_cited:
    #             tmp_cited_annotated = tmp_cited_annotated + "\n" + triple_data["head_name"][i] + "," + triple_data["edge_type"][
    #                 i] + "," + triple_data["tail_name"][i]
    #     annotated_data[key] = {"citing_data":tmp_citing_annotated, "cited_data":tmp_cited_annotated}
    label = ""
    paper_info = ".".join(paper.values()) # paper wokens in lower() form
    # print(paper_info)
    paper_tokens = paper_tokenizer(paper_info)
    for i in range(len(triple_data)):
        try:
            if triple_data["head_name"][i].lower() in paper_tokens and triple_data["tail_name"][i].lower() in paper_tokens:
                label = label+"("+triple_data["head_name"][i]+","+triple_data["edge_type"][i]+","+triple_data["tail_name"][i]+");"
        except Exception as e:
            print(e)
    annotated_paper = {"paper":paper_info,"triple":label}
    return annotated_paper


def dump_data(root_dir, triple_path):
    triple_data = get_triple(triple_path)
    total_num = 0
    for paper_dir in os.listdir(root_dir):
        if paper_dir.startswith("PMC") and paper_dir.endswith("xxxxxx"):
            total_num += len(os.listdir(os.path.join(root_dir, paper_dir)))
    with tqdm(total=total_num) as pbar:
        pbar.set_description("data_prerprocessing:")
        for paper_dir in os.listdir(root_dir):
            if paper_dir.startswith("PMC") and paper_dir.endswith("xxxxxx"):
                for paper_path in os.listdir(os.path.join(root_dir,paper_dir)):
                    paper = get_paper_info(os.path.join(root_dir, paper_dir, paper_path))
                    annotated_paper = triple_annotator(triple_data, paper)
                    if annotated_paper["triple"] is not "":
                        if os.path.exists(r"data/annotated_paper.json"):
                            with open("data/annotated_paper.json", "a", encoding="utf-8") as f:
                                json.dump(annotated_paper, f, indent=0)
                                # print("dump success")
                                pbar.update(1)
                        else:
                            with open("data/annotated_paper.json", "w", encoding="utf-8") as f:
                                json.dump(annotated_paper, f, indent=0)

if __name__=="__main__":
    dump_data(root_dir,triple_path)
