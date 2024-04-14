from pprint import pprint
import json
from court_parser import Parser
from spacy_extractor import SpacyExtractor
import os



doc_name = './test_documents/A03-3155-2020_20200429_Reshenija_i_postanovlenija.pdf'
doc_name2 = './train_documents/2 ответчика.pdf'

doc_name3 = os.path.join(os.path.dirname(__file__), 'test_documents/A83-19868-2020_20201207_Opredelenie (1).pdf')

main_model = os.path.join(os.path.dirname(__file__),'spacy_models/output237/model-best')
sums_model = os.path.join(os.path.dirname(__file__),'spacy_models/output237_sums/model-last')

parser = Parser(main_model,sums_model)

# print("***REGEX***")
# dop_info = parser.extract_info_regex(doc_name3)
# pprint(dop_info)

print("***SPACY***")

text = parser.extract_raw_page(0, doc_name3)
data = parser.extract_info_spacy(text,doc_name3)
pprint(json.loads(data))


