import json
import os
import networkx as nx
import dgl
import scispacy, spacy
from collections import Counter
from torch.utils.data import Dataset


class data_set(Dataset):
    def __int__(self, data_path, max_length):
        super(data_set, self).__int__()
        self.data_path = data_path
        self.data = None
        self.INTER_EDGE = 0
        self.INTRA_EDGE = 1
        try:
            self.nlp = spacy.load("en_ner_bionlp13cg_md") # For tokenize and entity graph building
        except Exception as e:
            print(e)
            print("Please Using 'en_ner_bionlp13cg_md' version")
        self.max_length = max_length

        if os.path.exists(data_path):
            with open(data_path, "r", encoding="utf-8") as f:
                try:
                    self.data = json.load(data_path)
                except Exception as e:
                    print(e)
        else:
            pass

        for i, data_item in enumerate(self.data):
            paper = data_item["paper"]
            label = data_item["triple"]

    def __getitem__(self, item):
        pass

    def __len__(self):
        pass

    def create_graph(self):
        pass

    def tokenizer(self, text):
        doc = self.nlp(text)
        entity_list = doc.ents
        # retokenize based on entity_list
        tokens_ = []
        with doc.retokenize() as retokenizer:
            for ent in doc.ents:
                retokenizer.merge(doc[ent.start:ent.end])
        for token in doc:
            tokens_.append(token)

        # miss the part of cut the sentence
        tokens = "[CLS]"+tokens_+"[SEP]"
        return entity_list, tokens




# def word2id(self, corpus):
#     bag_of_words = self.word_tokenizer(corpus)
#     count = sorted(self.counter(bag_of_words))
#     words = list(count.keys())
#     word2id = zip(words, range(len(words)))
#     with open(os.path(self.root, "word2id.json"), "w") as f:
#         json.dump(word2id, f)

# def rel2id(self, relation):
#     counter = Counter(relation)
#     rel2id = dict()
#     for i, j in zip(counter.keys(), range(len(counter.keys()))):
#         rel2id[i] = "R"+str(j)
#     # with open(os.path(self.root, "rel2id.json"), "w") as f:
#     #     json.dump(rel2id, f)
#     return rel2id
#
# # entity type embedding
# def etype2vec(self, entity_ls):
#     pass
#
# # word embedding
# def word2vec():
#     pass

