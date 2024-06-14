import spacy
from text_processor import TextProcessor
from regex_extractor import RegexExtractor
from datetime import datetime
from spacy_extractor import SpacyExtractor
import fitz
import os
import io
import json
import pymorphy3
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class Parser:
    """Класс описывающий разбор документов"""

    def __init__(self, main_model_path, sum_model_path) -> None:
        self.spacy_extractor = SpacyExtractor(main_model_path, sum_model_path)

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
            text+=t
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
        
        for key,item in parties.items():
            for party_num in range(len(item)):
                value = item[party_num]['PARTY']
                normalized_party = []
                for p in value.split(' '):
                    try:
                        parsed_phrase = morph.parse(p)[0]
                        if 'neut' in parsed_phrase.tag or 'datv' in parsed_phrase.tag and not 'masc' in parsed_phrase.tag:
                            parsed_phrase = parsed_phrase.inflect({'nomn'})
                        
                        
                        normalized_party.append(parsed_phrase.word)

                    except Exception as e:
                        print(f'Error:{e}')
                
                normalized_party = ' '.join(normalized_party)
                #normalized_party = TextProcessor.clear_result(normalized_party)
                parties[key][party_num]['PARTY'] = normalized_party
        
    def _extract_decision(self, doc_path):
        text = self.extract_all_pages(doc_path)
        decision = RegexExtractor.extract_decision(text)
        return decision

    def extract_info_spacy(self, text, doc_path):
        #TODO normalize parties
        case_date_num = self._find_case_number(doc_path)
        decision = self._extract_decision(doc_path)

        case_date_num = {
            "CASE_NUMBER": case_date_num.get('CaseNumber') if case_date_num else None,
            "CASE_DATE": case_date_num.get('CaseDate') if case_date_num else None
        }
        court_info = self.spacy_extractor.extract_all(text)
        spacy_result = court_info | case_date_num | decision
        #self._normalize_party(spacy_result['PARTIES'])
        #parties = spacy_result['PARTIES']
        
        return json.dumps(spacy_result, ensure_ascii=False)

    def text_from_images(self, doc_path):
        text = ''
        doc = fitz.open(doc_path)

        for i in range(len(doc)):
            for img in doc.get_page_images(i):
                xref = img[0]
                
                pix = fitz.Pixmap(doc, xref)
                img_bytes = pix.tobytes()
                text+=pytesseract.image_to_string(Image.open(io.BytesIO(img_bytes)), lang='rus')

        return text
