import spacy
from regex_extractor import RegexExtractor
import json
from difflib import SequenceMatcher
from text_processor import TextProcessor

SIMILARITY_RATE = 0.7

class SpacyExtractor:
    """Класс для извлечения данных с помощью моделей nlp SpaCy"""

    def __init__(self, main_model_path, sums_model_path) -> None:
        self.model_path = main_model_path
        self.sums_model_path = sums_model_path
        self.sums_doc = None
        self.general_info_doc = None

    def _find_docs(self, text):
        """Извлечение сущностей суда и сумм"""
        nlp_general_info = spacy.load(self.model_path)
        nlp_sums = spacy.load(self.sums_model_path)

        self.general_info_doc = nlp_general_info(text)
        self.sums_doc = nlp_sums(text)
    
    def _find_parties(self, doc):
        """Извелечение сторон"""
        parties = {'PLAINTIFFS':[],
                   'DEFENDANTS':[],
                   'THIRD-PARTY':[]}

        ks = []

        found_requisites = set()
        found_parties = set()

        for token in doc:
            if token.text.strip() == 'к':
                ks.append((token.text,token.idx))

        for e in range(len(doc.ents)):
            party = {'REQUISITES':None}

            if doc.ents[e].label_ == "PARTY":
                side = 'PLAINTIFFS'
                for k in ks:
                    if doc.ents[e].start_char > k[1]:
                        side = 'DEFENDANTS'

                
                party['PARTY'] = doc.ents[e].text

                if doc.ents[e+1].label_ == "REQUISITES":
                    party['REQUISITES'] = self._extract_requisites(doc.ents[e+1].text)


                self._add_party(parties=parties,
                                side=side, 
                                party=party,
                                found_parties=found_parties,
                                found_requisites=found_requisites,
                                is_third_party=False)
                

            elif doc.ents[e].label_ == "THIRD-PARTY":
                side = 'THIRD-PARTY'
                party = {'REQUISITES':None}
                party[side] = doc.ents[e].text

                if doc.ents[e+1].label_ == "REQUISITES":
                    party['REQUISITES'] = self._extract_requisites(doc.ents[e+1].text)
                
                self._add_party(parties=parties,
                                side=side, 
                                party=party,
                                found_parties=found_parties,
                                found_requisites=found_requisites,
                                is_third_party=True)


        return parties

    def _add_party(self, parties, side, party, found_requisites, found_parties, is_third_party):
        """Добавление стороны с проверкой на дубликат"""
        dublicate = False

        if party['REQUISITES'] and any(party['REQUISITES']):
            #Если есть любой реквизит, то проверить в найденных реквизитах
            for key,req in party['REQUISITES'].items():
                if req and req in found_requisites:
                    dublicate = True
                    break
                else:
                    found_requisites.add(req)
                    
        
        else:
            #Если нет реквизитов, проверить на похожесть в найденных участниках
            for found_party in found_parties:
                if is_third_party:
                    if SequenceMatcher(None, party['THIRD-PARTY'],found_party).ratio() > SIMILARITY_RATE:
                        dublicate = True
                        break
                else:
                    if SequenceMatcher(None, party['PARTY'],found_party).ratio() > SIMILARITY_RATE:
                        dublicate = True
                        break
            
        if is_third_party:
            found_parties.add(party['THIRD-PARTY'])
        else:
            found_parties.add(party['PARTY'])
                    


        if not dublicate:
            parties[side].append(party)
        
    def extract_all(self, text):
        """Извлечение всей информации из текста документа"""
        self._find_docs(text)

        res = {'PARTIES': self._find_parties(self.general_info_doc),
               'COURT_INFO': self._extract_court_info(self.general_info_doc),
               'SUMS': self._find_sums(self.sums_doc)}

        return res

    def _extract_court_info(self, doc):
        """Извлечение сути дела, суда, судьи"""
        result = {
            "CAUSE":[], 
        }

        for ent in doc.ents:
            if ent.label_ == 'CAUSE':
                result[ent.label_].append(ent.text)  
            if ent.label_ == 'COURT':
                result['COURT'] = RegexExtractor.find_court(ent.text)
                #result['COURT'] = TextProcessor.clear_result(court)
            elif ent.label_ == 'JUDGE':
                result['JUDGE'] = ent.text

        return result
    
    def _find_sums(self,doc):
        """Сбор значений и тегов сумм"""
        return [{'label':ent.label_, 'value':ent.text} for ent in doc.ents]

    def _extract_requisites(self,text):
        """Извлечение реквизитов из общей кучи regex-ом"""
        return RegexExtractor.extract_requisites(text)