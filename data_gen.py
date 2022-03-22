import json
import os
import networkx as nx
import dgl
import scispacy, spacy
from collections import Counter
from torch.utils.data import Dataset
from transformers import BertTokenizer
import Config

# Create dataset for Dataloader and model
class data_set(Dataset):
    def __int__(self, data_path, max_length, Config):
        super(data_set, self).__int__()
        self.data_path = data_path
        self.data = None
        self.INTER_EDGE = 0
        self.INTRA_EDGE = 1
        self.config = Config
        self.tokenizer = BertTokenizer.from_pretrained(self.config.bio_bert_path)
        try:
            self.nlp = spacy.load("en_ner_bionlp13cg_md") # For tokenize and entity graph building
        except Exception as e:
            print(e)
            print("Please Using 'en_ner_bionlp13cg_md' version")
        self.max_length = max_length

        if os.path.exists(self.data_path):
            with open(self.data_path, "r", encoding="utf-8") as f:
                try:
                    ori_data = json.load(data_path)
                except Exception as e:
                    print(e)
        else:
            pass

        # slef.data[index] = [{graph:graph, paper: {abstract:{}, intro:{}, citances:{}}, label:triple}]

        for i, data_item in enumerate(ori_data):
            doc = self.nlp(data_item["paper"][""])
            paper = data_item["paper"]
            label = data_item["triple"]




    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def create_graph(self, doc):
        entity_list, _, input_ids = self.tokenize(doc)
        graph = dgl.graph()


    def tokenize(self, doc):
        # doc = self.nlp(text)
        entity_list = {}
        entities = []
        # retokenize based on entity_list
        tokens_list = []
        # add new tokens if they're not in the vocab
        new_tokens = []
        with doc.retokenize() as retokenizer:
            for ent in doc.ents:
                retokenizer.merge(doc[ent.start:ent.end])
                entities.append(str(ent))
        # miss the part of cut the sentence
        # for token in doc:
        #     tokens_list.append(token)
        for sent in enumerate(doc.sents):
            for token in sent:
                tokens_list.append(str(token))
                tokens_list = tokens_list+["[SEP]"]
        tokens_list = ["CLS"] + tokens_list
        ids = self.tokenizer.convert_tokens_to_ids(tokens_list)
        for i, id in enumerate(ids):
            if id==100:
                if tokens_list[i] in entities:
                    new_tokens.append(tokens_list[i])
        self.tokenizer.add_tokens(new_tokens)
        input_ids = self.tokenizer.convert_tokens_to_ids(tokens_list)

        for i, token in enumerate(tokens_list):
            if token in entities:
                entity_list[token]==ids[i]

        return entity_list, tokens_list, input_ids     # dic, list, list




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

