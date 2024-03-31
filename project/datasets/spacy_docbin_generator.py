import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json
from spacy.tokens import SpanGroup, Span

nlp = spacy.blank('ru')
db = DocBin()
import time


f = open('datasets/238_cleared.json', 'r', encoding='utf-8')
train_data = json.load(f)[200:250]

# with open('datasets/238_cleared.json', 'w', encoding='utf-8') as f:
#     data = []
#     for document in tqdm(train_data):
#         labels = []
#         for label in document['label']:
#             if label['labels'][0] not in ('DEBT','FEE','PENALTY','PENNY','LOSS','PERCENTS','SUM','INTELLECTUAL-DEBT','MORAL-EXPENSES','COMPENSATION','FORFEIT','DEBT-PART','UNJUST-ENRICHMENT'):
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
        print(label['labels'][0])
        span = doc.char_span(label['start'], label['end'], label=label['labels'][0], alignment_mode='contract')

        if span is not None:
            spans.append(span)

    # group = SpanGroup(doc, name="sc", spans=spans)
    # #print(spans)
    doc.ents=spans
    # doc.spans["sc"] = group
    db.add(doc)
    
db.to_disk('./label_studio_valid_237.spacy')
