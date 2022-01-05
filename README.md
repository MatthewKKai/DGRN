# ER_Biomedical_Paper
Explainable Biomedical Paper Recommendation
We consider extracting information and link them from MeSH and generate triple which indicates the relation of entities.
Further steps span around reason generation and citation network information as prior probability for special recommendation.
Citation Context Analysis


## Extractor:
Extractor Settings:
Tokenizer + BertSeqClassification
Graph based model
Data Augmentation
SDP for better selection

Negative Samples and data masks

## Generator
Generator Settings:
Data Augmentation + Encoder-Decoder
