import spacy
from preprocessor import Preprocessor
from regex_extractor import RegexExtractor
from datetime import datetime
from spacy_extractor import SpacyExtractor
import fitz
import os
import json


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
    
    def extract_info_spacy(self, text):
        return json.dumps(self.spacy_extractor.extract_all(text), ensure_ascii=False)


