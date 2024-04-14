import spacy
from preprocessor import Preprocessor
from regex_extractor import RegexExtractor
from datetime import datetime
from spacy_extractor import SpacyExtractor
import fitz
import os
import json
import pymorphy3



class Parser:
    """Класс описывающий разбор документов"""
    pre = Preprocessor()
    

    def __init__(self, main_model_path, sum_model_path) -> None:
        self.spacy_extractor = SpacyExtractor(main_model_path, sum_model_path)

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
    

    def extract_info_regex(self, doc_path):
        #case_num = RegexExtractor.find_case(self._extract_raw_page(0, doc_path))
        case_date_num = self._find_case_number(doc_path)
        
        court = RegexExtractor.find_court(self.extract_raw_page(0, doc_path))
        cause = RegexExtractor.find_cause(self.extract_raw_page(0, doc_path))
        parties = RegexExtractor.find_parties(self.extract_raw_page(0, doc_path))
        return {
            "CaseNumber": case_date_num.get('CaseNumber') if case_date_num else None,
            "CaseDate": case_date_num.get('CaseDate') if case_date_num else None,
            "Court": court,
            "Causes": cause,
            "Parties": parties,
        }
    
    def _normalize_party(self, parties):
        morph = pymorphy3.MorphAnalyzer()
        normalized_parties = []
        for key,values in parties.items():
            
            for p in values:
                value = p['PARTY']      
                try:
                    normalized_party = []
                    parsed_phrase = morph.parse(value)[0]
                    if 'neut' in parsed_phrase.tag or 'datv' in parsed_phrase.tag and not 'masc' in parsed_phrase.tag:
                        parsed_phrase = parsed_phrase.inflect({'nomn'})
                    
                    normalized_party.append(parsed_phrase.word)

                    

                except Exception as e:
                    print(f'Error:{e}')

            normalized_parties[key]['PARTY'].append(normalized_party)
        

    def extract_info_spacy(self, text, doc_path):
        #TODO normalize parties
        case_date_num = self._find_case_number(doc_path)
        case_date_num = {
            "CASE_NUMBER": case_date_num.get('CaseNumber'),
            "CASE_DATE": case_date_num.get('CaseDate')
        }
        spacy_result = self.spacy_extractor.extract_all(text) | case_date_num

        #parties = spacy_result['PARTIES']
        #print(self._normalize_party(parties))
        return json.dumps(spacy_result, ensure_ascii=False)


