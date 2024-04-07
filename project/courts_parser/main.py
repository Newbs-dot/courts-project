from pprint import pprint
import json
from court_parser import Parser
from spacy_extractor import SpacyExtractor


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
parser = Parser('./spacy_models/output237/model-best')


dop_info = parser.extract_info_regex(doc_name)
#parties = parser._find_parties(doc_name2)
text = parser.extract_raw_page(0, doc_name)

print("***REGEX***")
pprint(dop_info)

print("***SPACY***")
spacy_extractor = SpacyExtractor('./spacy_models/output237/model-best','./spacy_models/output237_sums/model-last')



data = spacy_extractor.extract_all(text)



data = json.loads(data)
pprint(data)








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
