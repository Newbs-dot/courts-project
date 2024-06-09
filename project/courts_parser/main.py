from pprint import pprint
import json
from court_parser import Parser
from spacy_extractor import SpacyExtractor
import os



doc_name = './test_documents/A03-3155-2020_20200429_Reshenija_i_postanovlenija.pdf'
doc_name2 = './train_documents/2 ответчика.pdf'

doc_name3 = os.path.join(os.path.dirname(__file__), 'test_documents/A83-19868-2020_20201207_Opredelenie (1).pdf')

doc_test = os.path.join(os.path.dirname(__file__), 'test_documents/A03-3155-2020_20200429_Reshenija_i_postanovlenija.pdf')
doc_test2 = os.path.join(os.path.dirname(__file__), 'test_documents/A02-2390-2023_20231228_Reshenija_i_postanovlenija.pdf')
doc_test3 = os.path.join(os.path.dirname(__file__), 'test_documents/A40-5590-2023_20230424_Reshenija_i_postanovlenija.pdf')
doc_test_third_party = os.path.join(os.path.dirname(__file__), 'test_documents/A07-26467-2019_20211224_Reshenija_i_postanovlenija.pdf')

doc_w_img = os.path.join(os.path.dirname(__file__), 'test_documents/pdf_with_img.pdf')
main_model = os.path.join(os.path.dirname(__file__),'spacy_models/output237/model-best')
sums_model = os.path.join(os.path.dirname(__file__),'spacy_models/output237_sums/model-last')


parser = Parser(main_model,sums_model)

# print("***REGEX***")
# dop_info = parser.extract_info_regex(doc_name3)
# pprint(dop_info)

print("***SPACY***")


text = parser.extract_raw_page(0,doc_test3)
text += parser.text_from_images(doc_test3)
#print(text)

data = parser.extract_info_spacy(text,doc_test3)


pprint(json.loads(data))


