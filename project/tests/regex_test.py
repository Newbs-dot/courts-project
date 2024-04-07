import re
from difflib import SequenceMatcher
INN = re.compile(r'ИНН:?\s+(\d{10}|\d{12})\b', flags = re.MULTILINE | re.IGNORECASE)
KPP = re.compile(r'КПП:?\s+(\d{9})\b', flags = re.MULTILINE | re.IGNORECASE)
OGRN = re.compile(r'(ОГРН|ОГРНИП):?\s+(\d{13}|\d{15})\b', flags = re.MULTILINE | re.IGNORECASE)


def find_req(text):
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

print(find_req('ОГРН 1231296060069, КПП   111111111'))


    
print(SequenceMatcher(None, 'Федерального государственного унитарного предприятия «Охрана»',
                      'Федеральное государственное унитарное предприятие «Охрана»').ratio())