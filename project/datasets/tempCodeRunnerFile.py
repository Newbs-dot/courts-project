for document in tqdm(train_data):
#     text = document['text']
#     doc = nlp.make_doc(text)

#     spans = []

#     for label in document['label']:
#         print(label['labels'][0])
#         span = doc.char_span(label['start'], label['end'], label=label['labels'][0], alignment_mode='contract')

#         if span is not None:
#             spans.append(span)

#     # group = SpanGroup(doc, name="sc", spans=spans)
#     # #print(spans)
#     doc.ents=spans
#     # doc.spans["sc"] = group
#     db.add(doc)
    
# db.to_disk('./label_studio_valid_237.spacy')