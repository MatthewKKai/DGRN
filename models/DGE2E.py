import numpy as np
import pandas as pd
import scispacy
import spacy
import torch
from torch import nn
import transformers
from transformers import BertModel
import dgl
import Config


class DGE2E_Encoder(nn.Module):
    def __init__(self,Config):
        self.config = Config
        self.bio_bert = BertModel.from_pretrained(self.config.bio_bert_path)



    def encde(self):
        pass


class DGE2E_Decoder(nn.Moudle):
    def __int__(self):
        pass

    def decoe(self):
        pass


