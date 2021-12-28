# ER_Biomedical_Paper
Explainable Biomedical Paper Recommendation
We consider extracting information and link them from MeSH and generate triple which indicates the relation of entities.
Further steps span around reason generation and citation network information as prior probability for special recommendation.


Extractor Settings:
Tokenizer + BertSeqClassification
Seq2Seq Wrap
Data Augmentation

Negative Samples and data masks

Generator Settings:
Data Augmentation + Encoder-Decoder
