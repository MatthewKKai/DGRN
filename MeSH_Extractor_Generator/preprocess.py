import json
import pandas as pd
import numpy as np

json_path = r"data/cancer_corpus.json"
with open(json_path, encoding = "utf-8") as f:
    data = json.load(f)
    i = 0
    for key0 in data.keys():
        temp = data[key0]
        for tmp_data in temp:
            i = i + 1
            if i<200:
                try:
                    citing_abstract = re.search("p>.*</p", tmp_data["citing_abstract"]).group().strip("p>").strip("</p")
                    cited_abstract = re.search("p>.*</p", tmp_data["cited_abstract"]).group().strip("p>").strip("</p")
                    print("Citing_Abstract:{0}\n----\nCited Abstract:{1}\n****\n".format(citing_abstract,cited_abstract))
                except Exception as e:
                    pass
            else:
                break