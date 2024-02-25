import json

with open('./datasets/100_dataset.json',encoding='utf-8') as f:
  dataset = json.load(f)



dataset = dataset['annotations'][70:101]
print(len(dataset))

# for annotation in dataset:
#   print(annotation)

import pandas as pd
import os
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin


nlp = spacy.load("ru_core_news_lg")

db = DocBin() # create a DocBin object

for text, annot in tqdm(dataset): # data in previous format
    doc = nlp.make_doc(text) # create doc object from text
    ents = []
    for start, end, label in annot["entities"]: # add character indexes
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    doc.ents = ents # label the text with the ents
    db.add(doc)

db.to_disk("./test.spacy") # save the docbin object


