import os
import nltk
import numpy as np
import json
import collections
import torch
from torch import nn
from transformers import BertTokenizer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from tensorflow.data import Dataset

class data_loader(Dataset):
    def __init__(self, root, file_name):
        self.root = self.root
        with open(os.path.join(root, file_name), "r") as f:
            self.raw_data = f.read()
        self.doc_rel_pair = self.raw_data.split("\n")
        self.length = len(self.doc_rel_pair)
        self.counter = collections.Counter
        self.word_tokenizer = nltk.word_tokenize
        self.sent_tokenizer = nltk.sent_tokenize



    def __getitem__(self, item):

        pass

    def __len__(self):
        return self.length

    def split_data_label(self):
        corpus = ""
        relations = ""
        for pair in self.doc_rel_pair:
            tmp = pair.split("*****")
            try:
                corpus = corpus + " " + tmp[0]
                relations = relations + " " + tmp[1]
            except Exception as e:
                print(e)
                return corpus, relations
        return corpus, relations

    def word2id(self, corpus):
        bag_of_words = self.word_tokenizer(corpus)
        count = sorted(self.counter(bag_of_words))
        words = list(count.keys())
        word2id = zip(words, range(len(words)))
        with open(os.path(self.root, "word2id.json"), "w") as f:
            json.dump(word2id, f)


    def rel2id(self, relation):
        bag_of_relations = word_tokenize(relation)
        count = sorted(self.counter(bag_of_relations))
        relations = list(count.keys())
        rel2id = zip(relations, range(len(relations)))
        with open(os.path(self.root, "rel2id.json"), "w") as f:
            json.dump(relations, f)

    def grab_position(self, text, head, tail):
        # muli-times appearance of one entity -> lack of relation explaination
        word_tokens = self.word_tokenize(text)
        head_i = 0
        tail_i = 0
        for index in len(word_tokens):
            if head == word_tokens[index]:
                head_i = index
            if tail == word_tokens[index]:
                tail_i = index
        position = [head_i, tail_i]
        return position

    def word_tokenize(self, text):
        word_tokens = self.word_tokenize(text)
        return word_tokens

    def sent_tokenize(self, text):
        sent_tokens = self.sent_tokenizer(text)
        return sent_tokens

