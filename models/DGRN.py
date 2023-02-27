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
from models import Dynamic_Graph_Generator


class DGRN_Encoder(nn.Module):
    def __init__(self,config):
        self.config = config
        self.bio_bert = BertModel.from_pretrained(self.config.bio_bert_path)
        self.dropout = nn.Dropout(self.config.dropout)
        self.dgg = Dynamic_Graph_Generator()


    def encde(self):
        pass


    def forward(self):
        pass


class DGRN_Decoder(nn.Moudle):
    def __int__(self, encoder, config):
        self.cell = nn.RNNCell()
        self.encoder = encoder
        self.config = config


    def decoe(self):
        pass

    def forward(self):
        pass


class Gated_Unit(nn.Module):
    def __init__(self, graph_rep, text_rep):
        pass

    def forward(self):
        pass


# class Attetntion(nn.Module):
#     def __init__(self, src_size, trg_size):
#         self.W = nn.Bilinear
#         self.softmax = nn.Softmax(dim=-1)
#
#     def forward(self, src, trg):
#         score = self.W(src.unsqueeze(0).expand(trg.size(0), -1), trg)
#         score = self.softmax(score)
#         value = torch.mm(score.permute(1, 0), trg)
#
#         return score.squeeze(0), value.squeeze(0)