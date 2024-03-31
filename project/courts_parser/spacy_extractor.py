import spacy


class SpacyExtractor:

    def __init__(self,model_path) -> None:
        self.model_path = model_path
        

    def find_tags_nlp(self, text):
        nlp = spacy.load(self.model_path)
        return nlp(text)
    
    def _find_parties(self, doc):
        """Извелечение сторон"""
        parties = {'PLAINTIFFS':[],
                   'DEFENDANTS':[],
                   'THIRD-PARTY':[]}

        ks = []
        for token in doc:
            if token.text.strip() == 'к':
                ks.append((token.text,token.idx))

        for e in range(len(doc.ents)):
            party = {'REQUISITE':None}

            if doc.ents[e].label_ == "PARTY":
                side = 'PLAINTIFFS'
                for k in ks:
                    if doc.ents[e].start_char > k[1]:
                        side = 'DEFENDANTS'

                
                party['PARTY'] = doc.ents[e].text

                if doc.ents[e+1].label_ == "REQUISITES":
                    party['REQUISITE'] = doc.ents[e+1].text
                
                parties[side].append(party)

            elif doc.ents[e].label_ == "THIRD-PARTY":
                side = 'THIRD-PARTY'
                party = {'REQUISITE':None}
                party[side] = doc.ents[e].text

                if doc.ents[e+1].label_ == "REQUISITES":
                    party['REQUISITE'] = doc.ents[e+1].text
                
                parties[side].append(party)


        return parties

    def extract_all(self,doc):
        parties = self._find_parties(doc)
        court_info = self._extract_court_info(doc)
        return parties | court_info

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