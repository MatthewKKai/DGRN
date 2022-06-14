import numpy as np
import pandas as pd
import scispacy
import spacy
import torch
from torch import nn
from transformers import BertModel, BertForMaskedLM, BertTokenizer, AdamW
import dgl
import Config
from .utils import RelGraphConvLayer, RelEdgeLayer, Attention


class DGE2E_Encoder(nn.Module):
    def __init__(self,config):
        self.config = config
        self.bio_bert = BertModel.from_pretrained(self.config.bio_bert_path)
        self.dropout = nn.Dropout(self.config.dropout)



    def encde(self):
        pass


    def forward(self):
        pass


class DGE2E_Decoder(nn.Moudle):
    def __int__(self, encoder, config):
        self.cell = nn.RNNCell()
        self.encoder = encoder
        self.config = config


    def decoe(self):
        pass

    def forward(self):
        pass



class Dynamic_Graph_Generator(nn.Module):
    def __init__(self, entity_ls, G_s, config):
        self.config = config
        self.es = entity_ls
        self.tokenizer = BertTokenizer.from_pretrained(self.config.bio_bert_path)
        self.masked_model = BertForMaskedLM.from_pretrained(self.config.bio_bert_path)
        # randomly mask entity and generate labels
        self.mask = np.random.randint(low=0, high=len(self.es), size=(0.2*len(entity_ls),))
        self.optim = AdamW(self.masked_model.parameters(), lr=5e-5)


    def forward(self):
        inputs =  self.tokenizer(self.es)
        # creating labels
        labels = torch.zeros(inputs.input_ids.detach().size())
        for i in range(len(self.es)):
            if i in self.mask:
                labels[i] = 1
        inputs["labels"] = torch.tensor(labels, dtype=torch.long)
        self.optim.zero_grad()
        outputs = self.masked_model(**inputs)
        loss = outputs.loss
        loss.backward()
        self.optim.step()

        return self.masked_model(**inputs)




class Attetntion(nn.Module):
    def __init__(self, src_size, trg_size):
        self.W = nn.Bilinear
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, src, trg):
        score = self.W(src.unsqueeze(0).expand(trg.size(0), -1), trg)
        score = self.softmax(score)
        value = torch.mm(score.permute(1, 0), trg)

        return score.squeeze(0), value.squeeze(0)