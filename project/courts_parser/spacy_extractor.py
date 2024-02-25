import spacy


class SpacyExtractor:
    
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