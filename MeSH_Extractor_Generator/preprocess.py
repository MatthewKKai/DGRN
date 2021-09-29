import pandas as pd
import numpy as np
import json

# Load data and preprocess

path_json = r"/Users/loaferzk/LoaferZK/Research/PhD/MeSH_based/data/cancer_corpus.json"
with open(path_json, "r") as f:
    file = json.load(f)
