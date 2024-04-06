import spacy
from preprocessor import Preprocessor
from regex_extractor import RegexExtractor
from datetime import datetime
from spacy_extractor import SpacyExtractor
import fitz
import os
from pprint import pprint
import json

class Parser:
    pre = Preprocessor()
    def __init__(self, model_path) -> None:
        self.model_path = model_path

    def extract_raw_page(self, page, doc_path):
        text = ''
        pdf = fitz.open(doc_path)

        page = pdf[page]
        text = page.get_text('text')
        text = self.pre.clear_text(text)

        return text
    
    def _find_case_number(self, doc_path):
        #Поиск в названии
        doc_name = os.path.basename(doc_path)
        if '_' in doc_name:
            doc_name = doc_name.split('_')
            case_num,case_date = doc_name[0], doc_name[1]

            case_date = datetime.strptime(case_date,"%Y%m%d").strftime("%d-%m-%Y")

            return {"CaseNumber": case_num, "CaseDate": case_date}
    
    def _find_case_date_num(self, doc_path):
        case_date_num = self._find_case_number(doc_path)
            #case_num = RegexExtractor.find_case(self._extract_raw_page(0, doc_path))
        if case_date_num:
            return {"CaseNumber": case_date_num.get('CaseNumber'), "CaseDate": case_date_num.get('CaseDate')}
    
    def _find_court(self, doc_path):
        #TODO find with yargy,etc
        court = RegexExtractor.find_court(self.extract_raw_page(0, doc_path))
        return court
    
    def _find_cause(self, doc_path):
        #TODO find with spacy
        cause = RegexExtractor.find_cause(self.extract_raw_page(0, doc_path))
        return cause
    
    def _find_parties(self, doc_path):
        cause = RegexExtractor.find_parties(self.extract_raw_page(0, doc_path))
        return cause

    def extract_info(self, doc_path):
        case_date_num = self._find_case_date_num(doc_path)
        court = self._find_court(doc_path)
        cause = self._find_cause(doc_path)
        parties = self._find_parties(doc_path)
        return {
            "CaseNumber": case_date_num.get('CaseNumber') if case_date_num else None,
            "CaseDate": case_date_num.get('CaseDate') if case_date_num else None,
            "Court": court,
            "Causes": cause,
            "Parties": parties,
        }


test_text2 = """
Арбитражный суд г. Москвы в составе:
Председательствующего судьи Федоровой Д.Н. (единолично),
при ведении протокола секретарем судебного заседания Бессарабовой О.В.
рассмотрев в открытом судебном заседании дело по иску
ВЫСШЕГО ИСПОЛНИТЕЛЬНОГО ОРГАНА ГОСУДАРСТВЕННОЙ ВЛАСТИ ГОРОДА МОСКВЫ-ПРАВИТЕЛЬСТВО МОСКВЫ (ОГРН: 1027739813507, ИНН: 7710489036), ДЕПАРТАМЕНТА ГОРОДСКОГО ИМУЩЕСТВА ГОРОДА МОСКВЫ (ОГРН: 1037739510423, ИНН: 7705031674) к ОТКРЫТОМУ АКЦИОНЕРНОМУ ОБЩЕСТВУ "УРАЛЬСКАЯ ГОРНО-МЕТАЛЛУРГИЧЕСКАЯ КОМПАНИЯ" (ОГРН: 1026600727713, ИНН: 6606013640)
третьи лица 1. Управление Росреестра по городу Москве, 2. Государственная
инспекция по контролю за использованием объектов недвижимости города Москвы,
3.Комитет государственного строительного надзора города Москвы
о признании помещения подвала и мансарды самовольной постройкой, о признании
права собственности"""
test_text = 'Арбитражный суд Новосибирской области в составе судьи Хлоповой А.Г., при ведении протокола судебного заседания помощником судьи Кодиловой А.Г., рассмотрев в открытом судебном заседании дело по иску акционерного общества "Сибирский Антрацит" (ОГРН 1025404670620) к обществу с ограниченной ответственностью фирма "ФАЛАР" (ОГРН 1034205007847) , обществу с ограниченной ответственностью фирма "MEMES"  о взыскании убытков, связанных с приобретением комплектующих деталей на некачественный товар грохот ГИСЛ-62 (верхние сита штампов яч25х25, нижн. сита шпальт. Щ 1,6мм) зав.№0115, поставленный по договору поставки от 31.07.2014 №ТП-31/07/14 в размере 1 329 208 руб. 64 коп., расходов на проведение досудебной экспертизы в размере 55 000 руб.,'

doc_name = './test_documents/A03-3155-2020_20200429_Reshenija_i_postanovlenija.pdf'
doc_name2 = './train_documents/2 ответчика.pdf'
parser = Parser('.\output237\model-best')


dop_info = parser.extract_info(doc_name)
#parties = parser._find_parties(doc_name2)
text = parser.extract_raw_page(0, doc_name)

print("***REGEX***")
pprint(dop_info)

print("***SPACY***")
spacy_extractor = SpacyExtractor('.\output237\model-best','.\output237_sums\model-last')

doc = spacy_extractor.find_tags_nlp(text)
sums_doc = spacy_extractor.find_tags_sums(text)

data = spacy_extractor.extract_all(doc, sums_doc)



data = json.loads(data)
pprint(data)




#pprint(spacy_extractor.extract_all(doc))






# with open('test_data.txt','a',encoding='utf-8') as f: 
#     for root, dirs, files in os.walk(os.path.abspath("./train_documents")):
#         for file in files:
#             path = os.path.join(root, file)
#             parser = Parser('./')
#             text = parser._extract_raw_page(1,path)
#             text += parser._extract_raw_page(2,path)[:1000]
            
#             clear_text = preprocessor.clear_text(text)
#             f.write(f'{counter},{clear_text}\n')
        

# f.close()


