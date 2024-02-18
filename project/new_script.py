import re
from pprint import pprint
import glob
import fitz
import json

example = """
Арбитражный суд Тульской области
300041, г. Тула, Красноармейский проспект, д.5.
тел./факс (4872) 250-800; e-mail: а68.info@arbitr.ru; http://www.tula.arbitr.ru
Именем Российской Федерации
Р Е Ш Е Н И Е
г. Тула Дело  А68-7648/2022
Резолютивная часть решения изготовлена 20 декабря 2022 г.
Решение изготовлено в полном объеме 26 декабря 2022 г.
Арбитражный суд Тульской области в составе: Судьи Нестеренко С.В., при ведении
протокола секретарем судебного заседания Паршиковой О.Г., рассмотрев в открытом
судебном заседании исковое заявление Акционерного общества "Тулагорводоканал" (ИНН7105504223, ОГРН 1087154028004, 300001 г. Тула ул. Демидовская плотина д.8 ) (далее –
истец, АО «Тулагорводоканал») к акционерному обществу "ТАНДЕР" (ИНН 2310031475,
ОГРН 1022301598549, 350002 г. Краснодар, ул. Леваневского д.185) (далее – ответчик, АО
«Тандер») о взыскании задолженности в размере 820 755 рублей 22 копеек,
"""


def clear_newline_symbols(text):
    return text.replace('\n', '') if text else ''

def cleanup_text(text):
    #Очищаем текст от лишних пробелов внутри слов и между ними
    whitespaces_between_characters = re.sub(r'(?<=\b\w)\s(?=\w\b)','', text)
    excess_whitespaces = re.sub(r'[ \t]+', ' ', whitespaces_between_characters)
    return excess_whitespaces

def find_court(text):
    pattern = re.compile(r'Арбитражный суд (.*?)(?=\d| в составе|$)', re.IGNORECASE)

    courts = []
    for match in re.finditer(pattern, text):
        courts.append(
            (
                match.group(1),
                *match.span(1),
                "court"
            )
        )
    return courts

def find_parties(text):
    #Находим истца и ответчика
    #old
    #(?:заявлени[юяе] |иску )(.*?) (?=\(ИНН|\(ОГРН|$).*? к \s*(.*) (?=\(ИНН|\(ОГРН|$)
    #(?:заявлени[юяе] |иску )(.*?) (?=\(ИНН|\(ОГРН|\(|$).*? [кК] (?:ответчику\s*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$)
    #(?:заявлени[юяе]:? |иску\s|истец[\s:–]*|взыскателя[\s:–]*)(.*?) (?=\(ИНН|\(ОГРН|\(|$).*? [кК] (?:ответчику[\s:–]*)?(?:заинтересованному лицу[\s:–]*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$).*?(?:треть[ие] лиц[ао][\s:–]*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$)?
    #(?:заявлени[юяе]:? |иску\s|истец[\s:–]*|взыскателя[\s:–]*)(.*?) (?=\(ИНН|\(ОГРН|\(|$).*? [кК] (?:ответчику[\s:–]*|ответчикам[\s:–]*)?(?:заинтересованному лицу[\s:–]*)?(.*?)(?=\(ИНН|\(ОГРН|\(|$).*?(?:треть[ие] лиц[ао][\s:–]*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$)?
    #(?:заявлени[юяе]:? |иску\s|истец[\s:–]*|взыскателя[\s:–]*)(.*?) (?=\(ИНН|\(ОГРН|\(|$).*? [кК] (?:ответчику[\s:–]*|ответчикам[\s:–]*)?(?:заинтересованному лицу[\s:–]*)?(.*?)(?=\(ИНН|\(ОГРН|\(|$).*?(?:треть[ие] лиц[ао][\s:–]*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$)?
    pattern = re.compile(r'(?:заявлени[юяе]:? |иску\s|истец[\s:–]*|взыскателя[\s:–]*)(.*?) (?=\(ИНН|\(ОГРН|\(|$).*? [кК] (?:ответчику[\s:–]*)?(?:заинтересованному лицу[\s:–]*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$).*?(?:треть[ие] лиц[ао][\s:–]*)?(.*?) (?=\(ИНН|\(ОГРН|\(|$)?',re.IGNORECASE)
    parties = []
    
    res = re.search(pattern,text)

    #res.group(1,2)
    if res:
        parties.append((res.group(1),*res.span(1),'participant'))
        parties.append((res.group(2), *res.span(2),'participant'))

    return parties

def find_inn(text):
    inn_pattern = re.compile(r'ИНН:?\s*?(\d{10}|\d{12})', re.IGNORECASE)
    inns = []
    
    for match in re.finditer(inn_pattern, text):
        if match:
            #"inn":match.group(1),
            inns.append((match.group(1),*match.span(1),'inn'))

    return inns

def find_sums(text):
    #(?:в размере |о взыскании)(\d[\d\s]*)(?: руб\.| рублей)
    #(?:в размере |о взыскании )(\d[\d\s]*)
    sum_pattern = re.compile(r'(?:в размере |о взыскании )(\d[\d\s\,\.]*)(?: руб\.| рублей)', re.IGNORECASE)
    sums = []

    for match in re.finditer(sum_pattern, text):
        if match:
            sums.append((match.group(1),*match.span(1),'sum'))
    
    return sums

def clear_text(text):
    text = clear_newline_symbols(text)
    text = cleanup_text(text)
    return text




def form_result(example):
    example = clear_text(example)
    enities = []
    
    enities.extend(find_court(example))
    enities.extend(find_parties(example))
    enities.extend(find_inn(example))
    enities.extend(find_sums(example))


    result = {'example':example,'entities':enities}

    return result

result = {'dataset':[]}
for name in sorted(glob.glob('test_documents/*')):
    #третьи лица не парсятся =(
    #не парсятся если нет инн
    print(f'doc:{name}')
    pdf = fitz.open(name)
    

    page = pdf.load_page(0)
    line = page.get_text('text')[:2000]
    line = clear_text(line)

    with open('test.txt','a',encoding='utf-8') as f:
        f.write(f'{line}\n')

    #entities = form_result(line)
    #pprint(entities)

    #result['dataset'].append(entities)



#with open('dataset.json','w',encoding='utf-8') as f:
#    f.write(json.dumps(result,ensure_ascii=False))