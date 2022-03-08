import torch
from torch import nn
import transformers
from transformers import BertModel
import dgl
import Config


class DGE2E_Encoder(nn.Module):
    def __init__(self):
        self.config = Config
        self.bert = BertModel.from_pretrained(self.config.bert_path)
        pass

    def encde(self):
        pass


class DGE2E_Decoder(nn.Moudle):
    def __int__(self):
        pass

    def decoe(self):
        pass