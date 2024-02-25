import spacy
from preprocessor import Preprocessor
from regex_extractor import RegexExtractor
from datetime import datetime
import fitz
import os

class Parser:
    

    def __init__(self, model_path) -> None:
        self.model_path = model_path

    def extract_raw_page(self, page_num, doc_path):
        pdf = fitz.open(doc_path)
        page = pdf.load_page(page_num)
        text = page.get_text('text')

        return text
    
    def find_case_number(self, doc_path):
        #Поиск в названии
        doc_name = os.path.basename(doc_path)
        if '_' in doc_name:
            doc_name = doc_name.split('_')
            case_num,case_date = doc_name[0], doc_name[1]

            case_date = datetime.strptime(case_date,"%Y%m%d").strftime("%d-%m-%Y")

            return {"CaseNumber":case_num, "CaseDate": case_date}
        
test_text2 = """
Арбитражный суд г. Москвы в составе:
Председательствующего судьи Федоровой Д.Н. (единолично),
при ведении протокола секретарем судебного заседания Бессарабовой О.В.
рассмотрев в открытом судебном заседании дело по иску
ВЫСШЕГО ИСПОЛНИТЕЛЬНОГО ОРГАНА ГОСУДАРСТВЕННОЙ ВЛАСТИ
ГОРОДА МОСКВЫ-ПРАВИТЕЛЬСТВО МОСКВЫ (ОГРН: 1027739813507, ИНН:
7710489036), ДЕПАРТАМЕНТА ГОРОДСКОГО ИМУЩЕСТВА ГОРОДА МОСКВЫ
(ОГРН: 1037739510423, ИНН: 7705031674)
к ОТКРЫТОМУ АКЦИОНЕРНОМУ ОБЩЕСТВУ "УРАЛЬСКАЯ ГОРНО-
МЕТАЛЛУРГИЧЕСКАЯ КОМПАНИЯ" (ОГРН: 1026600727713, ИНН: 6606013640)
третьи лица 1. Управление Росреестра по городу Москве, 2. Государственная
инспекция по контролю за использованием объектов недвижимости города Москвы,
3.Комитет государственного строительного надзора города Москвы
о признании помещения подвала и мансарды самовольной постройкой, о признании
права собственности"""
test_text = 'Арбитражный суд Новосибирской области в составе судьи Хлоповой А.Г., при ведении протокола судебного заседания помощником судьи Кодиловой А.Г., рассмотрев в открытом судебном заседании дело по иску акционерного общества "Сибирский Антрацит" (ОГРН 1025404670620) к обществу с ограниченной ответственностью фирма "ФАЛАР" (ОГРН 1034205007847) о взыскании убытков, связанных с приобретением комплектующих деталей на некачественный товар грохот ГИСЛ-62 (верхние сита штампов яч25х25, нижн. сита шпальт. Щ 1,6мм) зав.№0115, поставленный по договору поставки от 31.07.2014 №ТП-31/07/14 в размере 1 329 208 руб. 64 коп., расходов на проведение досудебной экспертизы в размере 55 000 руб.,'

doc_name = './test_documents/A83-19868-2020_20201207_Opredelenie (1).pdf'
parser = Parser('.\output\model-best')
page = parser.extract_raw_page(0,doc_name)
regex_extractor = RegexExtractor()
case = regex_extractor.find_case(page)
date = parser.find_case_number(doc_name)
court = regex_extractor.find_court(page)
cause = regex_extractor.find_cause(page)

print(case, date, court,cause)


