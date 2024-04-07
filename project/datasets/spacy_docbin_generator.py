import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json
from spacy.tokens import SpanGroup, Span

nlp = spacy.blank('ru')
db = DocBin()
import time


f = open('datasets/238_sums.json', 'r', encoding='utf-8')
train_data = json.load(f)[200:]

# with open('datasets/238_sums.json', 'w', encoding='utf-8') as f:
#     data = []
#     for document in tqdm(train_data):
#         labels = []
#         for label in document['label']:
#             if label['labels'][0] in ('DEBT','FEE','PENALTY','PENNY','LOSS','PERCENTS','SUM','INTELLECTUAL-DEBT','MORAL-EXPENSES','COMPENSATION','FORFEIT','DEBT-PART','UNJUST-ENRICHMENT'):
#                 labels.append(label)

#         data.append(
#             {
#                 "text":document['text'],"label":labels
#             })
        
#     f.write(json.dumps(data,ensure_ascii=False)) 
    

for document in tqdm(train_data):
    text = document['text']
    doc = nlp.make_doc(text)

    spans = []

    for label in document['label']:
        #print(label['labels'][0])
        span = doc.char_span(label['start'], label['end'], label=label['labels'][0], alignment_mode='contract')

        if span is not None:
            spans.append(span)

    # group = SpanGroup(doc, name="sc", spans=spans)
    # #print(spans)
    try:

        doc.ents=spans
    except:
        print(spans)
    # doc.spans["sc"] = group
    db.add(doc)
    
db.to_disk('./label_studio_valid_sums.spacy')




# import json

# with open('./datasets/100_dataset.json',encoding='utf-8') as f:
#   dataset = json.load(f)



# dataset = dataset['annotations'][70:101]
# print(len(dataset))

# # for annotation in dataset:
# #   print(annotation)

# import pandas as pd
# import os
# from tqdm import tqdm
# import spacy
# from spacy.tokens import DocBin


# nlp = spacy.load("ru_core_news_lg")

# db = DocBin() # create a DocBin object

# for text, annot in tqdm(dataset): # data in previous format
#     doc = nlp.make_doc(text) # create doc object from text
#     ents = []
#     for start, end, label in annot["entities"]: # add character indexes
#         span = doc.char_span(start, end, label=label, alignment_mode="contract")
#         if span is None:
#             print("Skipping entity")
#         else:
#             ents.append(span)
#     doc.ents = ents # label the text with the ents
#     db.add(doc)

# db.to_disk("./test.spacy") # save the docbin object


