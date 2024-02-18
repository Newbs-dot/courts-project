import spacy
from spacy.matcher import DependencyMatcher

nlp = spacy.load("ru_core_news_sm")
matcher = DependencyMatcher(nlp.vocab)

pattern = [
    {
        "RIGHT_ID": "anchor_founded",
        "RIGHT_ATTRS": {"NORM": "к"}
    },
     {
        "LEFT_ID": "anchor_founded",
        "REL_OP": "<",
        "RIGHT_ID": "founded_subject",
        "RIGHT_ATTRS": {"DEP": "nmod"},
    }

]

matcher.add("FOUNDED", [pattern])
doc = nlp("заявление компании база к ОАО СБЕРБАНК")
matches = matcher(doc)

print(matches) # [(4851363122962674176, [6, 0, 10, 9])]
# Each token_id corresponds to one pattern dict
match_id, token_ids = matches[0]

for i in range(len(token_ids)):
    print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)
