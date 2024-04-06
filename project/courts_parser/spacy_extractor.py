import spacy
from regex_extractor import RegexExtractor
import json
from difflib import SequenceMatcher


class SpacyExtractor:

    def __init__(self,main_model_path,sums_model_path) -> None:
        self.model_path = main_model_path
        self.sums_model_path = sums_model_path
        

    def find_tags_nlp(self, text):
        """Поиск общих тегов"""
        nlp = spacy.load(self.model_path)
        return nlp(text)
    
    def find_tags_sums(self, text):
        """Поиск тегов сумм"""
        nlp = spacy.load(self.sums_model_path)
        return nlp(text)
    
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
                                found_requisites=found_requisites)
                

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
                                found_requisites=found_requisites)


        return parties

    def _add_party(self, parties, side, party, found_requisites, found_parties):
        """Добавление стороны с проверкой на дубликат"""
        dublicate = False

        if any(party['REQUISITES']):
            #Если есть любой реквизит, то проверить в найденных реквизитах
            for key,req in party['REQUISITES'].items():
                if req and req in found_requisites:
                    dublicate = True
                    break
                else:
                    found_requisites.add(req)
        
        else:
            #Если нет реквизитов, проверить похожих в найденных участниках
            for found_party in found_parties:
                if SequenceMatcher(None, party['PARTY'],found_party).ratio() > 70:
                    dublicate = True
                    break
                else:
                    found_parties.add(party['PARTY'])
                    


        if not dublicate:
            parties[side].append(party)
        

    # def _exclude_parties(self, parties):
    # for party in side
    # check if party exists with same requisites or if no requisites then check with levenstein


    def extract_all(self, doc, doc_sums):
        """Извлечение информации из документа"""
        res = {'PARTIES': self._find_parties(doc),
               'COURT_INFO': self._extract_court_info(doc),
               'SUMS': self._find_sums(doc_sums)}

        return json.dumps(res, ensure_ascii=False)

    def _extract_court_info(self, doc):
        """Извлечение сути дела, суда, судьи"""
        result = {
            "COURT": [], 
            "JUDGE": [],
            "CAUSE":[], 
        }


        for ent in doc.ents:
            if ent.label_ in result.keys():
                result[ent.label_].append(ent.text)

        return result
    
    def _find_sums(self,doc):
        """Сбор значений и тегов сумм"""
        return [{'label':ent.label_, 'value':ent.text} for ent in doc.ents]

    def _extract_requisites(self,text):
        """Извлечение реквизитов из общей кучи regex-ом"""
        return RegexExtractor.extract_requisites(text)