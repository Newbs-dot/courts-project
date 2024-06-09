import re

INN = re.compile(r'ИНН:?\s+(\d{10}|\d{12})\b', flags = re.MULTILINE | re.IGNORECASE)
KPP = re.compile(r'КПП:?\s+(\d{9})\b', flags = re.MULTILINE | re.IGNORECASE)
OGRN = re.compile(r'(ОГРН|ОГРНИП):?\s+(\d{13}|\d{15})\b', flags = re.MULTILINE | re.IGNORECASE)
COURT = re.compile(r'Арбитражный суд\s+(.*?)(?=в составе|$|\d)',re.IGNORECASE)
DECISION = re.compile(r'(?:определил:|решил:)(.*?)\s+(?=решение арбитражного|определение|решение может быть)', re.IGNORECASE)


class RegexExtractor:
    """Класс для извлечения данных с помощью Regex"""
    @staticmethod
    def find_cause(text):
        #TODO интелелктуальной о запрете, split multiple causes
        pattern = r'о (взыскании|вынесении|признании|обязании|привлечении|запрете)(.*?)(?=при участии|представители|третье лицо|лица|руководствуясь|установил|без участия)'
        match = re.search(pattern,text, re.IGNORECASE)
        return match.group(0) if match else None
    
    @staticmethod
    def find_case(text):
        pattern = r'дело №\s*(.*?)(?:$|\s)'
        match = re.search(pattern,text, re.IGNORECASE)
        return match.group(1) if match else None
    
    @staticmethod
    def find_court(text):
        #TODO Интеллектуальный итд
        match = re.search(COURT,text)
        return match.group(0) if match else None
    
    @staticmethod
    def find_parties(text):
        #Находим предполагаемых истцов и ответчиков
        #old
        #(?:заявлени[юяе] |иску )(.*?) (?=\(ИНН|\(ОГРН|$).*? к \s*(.*) (?=\(ИНН|\(ОГРН|$)
        #(?:заявлени[юяе] |иску )(.*?) (?=\(ИНН|\(ОГРН|\(|$).*? [кК] (?:ответчику\s*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$)
        #(?:заявлени[юяе]:? |иску\s|истец[\s:–]*|взыскателя[\s:–]*)(.*?) (?=\(ИНН|\(ОГРН|\(|$).*? [кК] (?:ответчику[\s:–]*)?(?:заинтересованному лицу[\s:–]*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$).*?(?:треть[ие] лиц[ао][\s:–]*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$)?
        #(?:заявлени[юяе]:? |иску\s|истец[\s:–]*|взыскателя[\s:–]*)(.*?) (?=\(ИНН|\(ОГРН|\(|$).*? [кК] (?:ответчику[\s:–]*|ответчикам[\s:–]*)?(?:заинтересованному лицу[\s:–]*)?(.*?)(?=\(ИНН|\(ОГРН|\(|$).*?(?:треть[ие] лиц[ао][\s:–]*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$)?
        #(?:заявлени[юяе]:? |иску\s|истец[\s:–]*|взыскателя[\s:–]*)(.*?) (?=\(ИНН|\(ОГРН|\(|$).*? [кК] (?:ответчику[\s:–]*|ответчикам[\s:–]*)?(?:заинтересованному лицу[\s:–]*)?(.*?)(?=\(ИНН|\(ОГРН|\(|$).*?(?:треть[ие] лиц[ао][\s:–]*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$)?
        #pattern = re.compile(r'(?:заявлени[юяе]:? |иску\s|истец[\s:–]*|взыскателя[\s:–]*)(.*?) (?=\(ИНН|\(ОГРН|\(|$).*? [кК] (?:ответчику[\s:–]*)?(?:заинтересованному лицу[\s:–]*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$).*?(?:треть[ие] лиц[ао][\s:–]*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$)?',re.IGNORECASE)
        pattern =re.compile(r'(?:заявлени[юяе]:?\s+|иску\s+|истец[\s:–]*|взыскателя[\s:–]*)(.*?)\s+[кК]\s+(.*?)\s+о (взыскании|вынесении|признании|обязании|привлечении|запрете)',re.IGNORECASE)
        
        parties = {'PLAINTIFFS':[], 
                   'DEFENDANTS':[]}

        res = re.search(pattern,text)
        if res:
            parties['PLAINTIFFS'].append({'DATA': res.group(1),'SPAN': res.span(1)})
            parties['DEFENDANTS'].append({'DATA': res.group(2),'SPAN': res.span(2)})

        return parties
    
    @staticmethod
    def extract_decision(text):
        decision = re.search(DECISION,text)
        return {'DECISION':decision.group(1) if decision else None}


    @staticmethod
    def extract_requisites(text):
        inn = re.search(INN,text)
        kpp = re.search(KPP,text)
        ogrn = re.search(OGRN,text)
        req = {
            'ИНН':inn.group(1) if inn else None,
            'КПП':kpp.group(1) if kpp else None,
            'ОГРН':ogrn.group(2) if ogrn else None,
            #'Адрес':
        }
        return req



    

