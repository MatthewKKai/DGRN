import json
import os
import nltk
from nltk import word_tokenize, sent_tokenize


# def word2id(self, corpus):
#     bag_of_words = self.word_tokenizer(corpus)
#     count = sorted(self.counter(bag_of_words))
#     words = list(count.keys())
#     word2id = zip(words, range(len(words)))
#     with open(os.path(self.root, "word2id.json"), "w") as f:
#         json.dump(word2id, f)


def rel2id(self, relation):
    bag_of_relations = word_tokenize(relation)
    count = sorted(self.counter(bag_of_relations))
    relations = list(count.keys())
    rel2id = zip(relations, "R"+str(range(len(relations))))
    with open(os.path(self.root, "rel2id.json"), "w") as f:
        json.dump(relations, f)


def entity2type(self, entity_dict):
    pass
