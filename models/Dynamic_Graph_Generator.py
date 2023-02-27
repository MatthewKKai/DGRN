import dgl
import torch
import pandas as pd
from torch import nn, optim
from Config import get_opt
from transformers import BertModel, BertTokenizer, BertForMaskedLM
from models.utils import RelGraphConvLayer, RelEdgeLayer, get_cuda

# get configs and dirs
config = get_opt()
meta_dir = r"./data/static_graph.csv"
meta_sg = pd.read_csv(meta_dir, encoding="utf-8")

# create graph
src = meta_sg["head_name"]
dst = meta_sg["tail_name"]
static_graph = dgl.graph((src, dst))
static_graph = dgl.add_self_loop(static_graph)

# DGG
class Dynamic_Graph_Generator(nn.Module):
    def __init__(self, entity_ls, config):
        self.config = config
        self.es = entity_ls
        self.G_s = static_graph
        self.tokenizer = BertTokenizer.from_pretrained(self.config.bio_bert_path)
        self.masked_model = BertForMaskedLM.from_pretrained(self.config.bio_bert_path)
        self.graph_conv = RelGraphConvLayer()
        # randomly mask entity and generate labels
        self.optim = optim.AdamW(self.masked_model.parameters(), lr=5e-5)


    def forward(self):
        inputs =  self.tokenizer(self.es)
        # randomly mask 20%
        rand = torch.rand(inputs.input_ids.shape)
        mask = (rand<0.2)*(inputs.input_ids!=101)*(inputs.input_ids!=102)

        # creating labels
        labels = inputs.input_ids.detach().clone()
        inputs_ids = inputs["input_ids"]
        self.optim.zero_grad()
        outputs = self.masked_model(inputs_ids, attention_masks = mask, labels = labels)
        loss = outputs.loss
        loss.backward()
        self.optim.step()

        return self.masked_model(**inputs)