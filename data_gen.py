import json
import os
import nltk
from nltk import word_tokenize, sent_tokenize


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


def word_tokenize(self, text):
    word_tokens = self.word_tokenize(text)
    return word_tokens


def sent_tokenize(self, text):
    sent_tokens = self.sent_tokenizer(text)
    return sent_tokens

