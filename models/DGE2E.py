import numpy as np
import pandas as pd
import scispacy
import spacy
import torch
from torch import nn
from transformers import BertModel
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
        self.bio_bert = BertModel.from_pretrained(self.config.bio_bert_path)
        # randomly mask entity and generate labels
        self.labels = np.zeros(len(entity_ls))
        self.mask = np.random.randint(low=0, high=len(entity_ls), size=(0.2*len(entity_ls),))
        for i in range(len(entity_ls)):
            if i in self.mask:
                self.labels[i] = 1


    def forward(self):
        pass



class Attetntion(nn.Module):
    def __init__(self, src_size, trg_size):
        self.W = nn.Bilinear
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, src, trg):
        score = self.W(src.unsqueeze(0).expand(trg.size(0), -1), trg)
        score = self.softmax(score)
        value = torch.mm(score.permute(1, 0), trg)

        return score.squeeze(0), value.squeeze(0)