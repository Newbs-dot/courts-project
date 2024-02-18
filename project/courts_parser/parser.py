import spacy
from preprocessor import Preprocessor

class Parser:

    def __init__(self, model_path) -> None:
        self.model_path = model_path
    
    def find_tags_nlp(self, text):
        nlp = spacy.load(self.model_path)
        doc = nlp(text)

        return doc.ents
    
    def find_tags_regex(self, text):
        pass

text = 'Арбитражный суд Новосибирской области в составе судьи Хлоповой А.Г., при ведении протокола судебного заседания помощником судьи Кодиловой А.Г., рассмотрев в открытом судебном заседании дело по иску акционерного общества "Сибирский Антрацит" (ОГРН 1025404670620) к обществу с ограниченной ответственностью фирма "ФАЛАР" (ОГРН 1034205007847) о взыскании убытков, связанных с приобретением комплектующих деталей на некачественный товар грохот ГИСЛ-62 (верхние сита штампов яч25х25, нижн. сита шпальт. Щ 1,6мм) зав.№0115, поставленный по договору поставки от 31.07.2014 №ТП-31/07/14 в размере 1 329 208 руб. 64 коп., расходов на проведение досудебной экспертизы в размере 55 000 руб.,'

preprocessor = Preprocessor()
parser = Parser('.\output\model-best')

print(parser.find_tags_nlp(preprocessor.clear_text(text)))