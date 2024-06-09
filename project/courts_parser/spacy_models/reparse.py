import json

def load_data(file):
    with open (file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

docs = load_data("datasets/300_main.json")[240:]

data = []
for doc in docs:
    text = doc['text']
    entities = doc['label']

    ents = {'entities':[[e['start'],e['end'],e['labels'][0]] for e in entities]}
    res = [text,ents]




    data.append(res)

with open('courts_parser/spacy_models/reparsed.json', 'w',encoding='utf-8') as rep:
    rep.write(json.dumps(data,indent=4,ensure_ascii=False))