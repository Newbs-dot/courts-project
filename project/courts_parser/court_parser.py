from text_processor import TextProcessor
from regex_extractor import RegexExtractor
from datetime import datetime
import fitz
import os
import io
import json


class Parser:
    """Класс описывающий разбор документов"""

    def extract_raw_page(self, page, doc_path):
        text = ''
        pdf = fitz.open(doc_path)

        page = pdf[page]
        text = page.get_text('text')
        text = TextProcessor.clear_text(text)

        return text
    
    def extract_all_pages(self, doc_path):
        text = ''
        pdf = fitz.open(doc_path)
        for p in range(pdf.page_count):
            page = pdf[p]
            t = page.get_text('text')
            t = TextProcessor.clear_text(t)
            text += t
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
        
    def _extract_decision(self, doc_path):
        text = self.extract_all_pages(doc_path)
        decision = RegexExtractor.extract_decision(text)
        return decision
