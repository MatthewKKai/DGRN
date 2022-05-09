import json
import os
import networkx as nx
import dgl
import scispacy, spacy
from collections import Counter, defaultdict
from torch.utils.data import Dataset
from transformers import BertTokenizer
import Config

# Create dataset for Dataloader and model
class data_set(Dataset):
    def __int__(self, data_path, max_length, Config):
        super(data_set, self).__int__()
        self.data_path = data_path
        self.data = []
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

        # slef.data[index] = [{paper:{graph:graph, path:path_info, abstract:{}, intro:{}, citances:{}}, label:triple}]

        for i, data_item in enumerate(ori_data):
            paper = {}

            doc_paper = self.nlp(data_item["paper"]["abstract"] + data_item["paper"]["intro"] + data_item["paper"]["citances"])

            doc_abstract = None if data_item["paper"]["abstract"] is "" else self.nlp(data_item["paper"]["abstract"])
            doc_intro = None if data_item["paper"]["intro"] is "" else self.nlp(data_item["paper"]["intro"])
            doc_citances = None if data_item["paper"]["citances"] is "" else self.nlp(data_item["paper"]["citances"])

            # section info
            _, tokens_list_abs, input_ids_abs = self.tokenize(doc_abstract)
            _, tokens_list_intro, input_ids_intro = self.tokenize(doc_intro)
            _, tokens_list_cit, input_ids_cit = self.tokenize(doc_citances)

            # graph info
            graph, path = self.create_graph(doc_paper)

            # paper = data_item["paper"]
            # label = data_item["triple"]
            self.data.append({
                "abstract":{"tokens":tokens_list_abs, "input_ids":input_ids_abs},
                "intro":{"tokens":tokens_list_intro, "input_ids":input_ids_intro},
                "citances":{"tokens":tokens_list_cit, "input_ids":input_ids_cit},
                "graph":{"graph":graph, "path":path}
            })



    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def create_graph(self, doc, entity_dict):
        graph_store = defaultdict(list)
        entity_list = []
        rel_dcit = {}
        # get entities
        # ents = doc.ents
        # with doc.retokenize() as retokenizer:
        #     for ent in doc.ents:
        #         retokenizer.merge(doc[ent.start:ent.end])
        # for ent in ents:
        #     if str(ent) in entity_dict.keys():
        #         entity_list.append(ent)

        for sent in doc.sents:
            ents = sent.ents
            for ent in ents:
                if str(ent) in entity_dict.keys():
                    entity_list.append(ent)


        # one-hop expansion
        # for e in entity_list:
        #     pass

        # entities to ids and graph construction
        node = {}
        for i, e in enumerate(entity_list):
            node[e] = i

        edge = {}




        graph = dgl.heterograph(graph_store)




        # path construction
        path = dict()



        return graph, path, entity_list


    def tokenize(self, doc):
        # doc = self.nlp(text)
        entity_with_ids = {}
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
        tokens_list = ["[CLS]"] + tokens_list
        ids = self.tokenizer.convert_tokens_to_ids(tokens_list)
        for i, id in enumerate(ids):
            if id==100:
                if tokens_list[i] in entities:
                    new_tokens.append(tokens_list[i])
        self.tokenizer.add_tokens(new_tokens)
        input_ids = self.tokenizer.convert_tokens_to_ids(tokens_list)

        for i, token in enumerate(tokens_list):
            if token in entities:
                entity_with_ids[token]==ids[i]

        return entity_with_ids, tokens_list, input_ids     # dic, list, list

    # convert triple to ids
    def triple_to_ids(self, triple):
        pass



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

