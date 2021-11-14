import pandas as pd
import numpy as np
import json
from transformers import *

# Load data and preprocess

path_json = r".cancer_corpus.json"
with open(path_json, "r") as f:
    file = json.load(f)
