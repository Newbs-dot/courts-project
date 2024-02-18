import spacy
from preprocessor import Preprocessor
from regex_finder import RegexFinder
from datetime import datetime
import fitz

class Parser:

    def __init__(self, model_path, doc) -> None:
        self.model_path = model_path
        self.document = doc

    def extract_introduction(self):
        pdf = fitz.open(self.document)
        page = pdf.load_page(0)
        line = page.get_text('text')[:2000]

        return line
    
    def find_tags_nlp(self, text):
        nlp = spacy.load(self.model_path)
        doc = nlp(text)
        

        court_info = self.extract_court_info(doc)
        #print(ents)
        ents = [(e.text, e.label_) for e in doc.ents]
        return ents
        #result = {"Court":}
        #for ent in doc.ents:
        #    print(ent.text, ent.start_char, ent.end_char, ent.label_)
        #ents = [(e.text, e.label_) for e in doc.ents]
        
        
        #(e.text, e.label_)
        #for e in doc.ents


        #print(ents)
    def extract_court_info(self, doc):
        result = {
            "COURT": [],
            "JUDGE": [],
            "CAUSE":[],
            "SUM":[],
            "RESULT":[],
        }

        ents = doc.ents
        for ent in ents:
            if ent.label_ in result:
                result[ent.label_].append(ent.text)
        return result

    def extract_parties(self, ents):
        pass
    
    def find_case_number(self, doc_name):
        #Поиск в документе
        #finder = RegexFinder()
        #doc.toText()

        #Поиск в названии
        if '_' in doc_name:
            doc_name = doc_name.split('_')
            case_num,case_date = doc_name[0],doc_name[1]

            case_date = datetime.strptime(case_date,"%Y%m%d").strftime("%d-%m-%Y")

            return {"CaseNumber":case_num, "CaseDate": case_date}
    
    def parse_doc(nlp_tags, doc_name):
        result = {}
        return result


        
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

preprocessor = Preprocessor()
parser = Parser('.\output\model-best','.\test_documetns')

text = preprocessor.clear_text(test_text2)

print(parser.find_tags_nlp(text))