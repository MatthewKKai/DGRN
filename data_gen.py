import json
import os
import nltk
from collections import Counter
from nltk import word_tokenize, sent_tokenize


# def word2id(self, corpus):
#     bag_of_words = self.word_tokenizer(corpus)
#     count = sorted(self.counter(bag_of_words))
#     words = list(count.keys())
#     word2id = zip(words, range(len(words)))
#     with open(os.path(self.root, "word2id.json"), "w") as f:
#         json.dump(word2id, f)

def rel2id(self, relation):
    counter = Counter(relation)
    rel2id = dict()
    for i, j in zip(counter.keys(), range(len(counter.keys()))):
        rel2id[i] = "R"+str(j)
    # with open(os.path(self.root, "rel2id.json"), "w") as f:
    #     json.dump(rel2id, f)
    return rel2id

# entity type embedding
def etype2vec(self, entity_ls):
    pass

# word embedding
def word2vec():
    pass