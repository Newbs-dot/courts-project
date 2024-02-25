import glob
import re
import fitz
#from pdfminer.high_level import extract_pages, extract_text
import json
from collections import deque
from pprint import pprint
"""
Название суда:

1)есть название судов через перенос строки
2)вот такое А Р Б И Т Р А Ж Н Ы Й С У Д
3)в виде изображения
4)еще номерной аппеляционный

Паттерны истца/ответчика:

1) по заявлению 1 к 2 о ...
2) по иску 1 к 2 о ...
3) заявление 1 в лице 1.1 к 2 о ...
4) по исковому заявлению 1 к 2 о ...
5) заявления истца 1 к ответчику 2 об ...
6) по иску:
   истец: 1
   ответчик: 2
   о ...
7) по иску 1 к ответчику 2 о ...
8) по иску 1 к ответчику:2 о/об ...
9) по заявлению 1 к ответчику: 2
10) искового заявления 1 к 2 о ...
11) исковое заявления 1 к 2 о/об ...
12) по иску
    истец 1
    к ответчику 2 о ...
13) по заявлению 1 К ответчику 2 О ...

PS:
О/об может быть много
бывает что нет о в начале
TODO:
1) Графический интерфейс скармливающий док и отдающий результат?
    - Парсер доков по абзацам, разбор на абзацы
    - Доставать суд
    - двоеточия и переносы строки?????
    - Нормализатор
    - Извлечение реквизитов из полученных истца и ответчика
2) Датасет
3) Узнать про регулярки
"""

test_text = """
Огородный проезд, д. 5, стр. 2, Москва, 127254
http:/
АРБИТРАЖНЫЙ   СУД   АЛТАЙСКОГО   КРАЯ
656015, Барнаул, пр. Ленина, д. 76, тел.: (3852) 29-88-01
h
063/2019-45794(1)
"""

import re


def clear_newline_symbols(text):
    return text.replace('\n', '') if text else ''

def cleanup_text(text):
    #Очищаем текст от лишних пробелов внутри слов и между ними
    whitespaces_between_characters = re.sub(r'(?<=\b\w)\s(?=\w\b)','', text)
    excess_whitespaces = re.sub(r'[ \t]+', ' ', whitespaces_between_characters)
    return excess_whitespaces

def find_court(text):
    # извлекаем название суда

    """
    TODO
    * Вынести отдельно аппеляционный суд, суд по интеллектуальным правам
    * Можно добавить словарь всех судов для проверки
    """

    #pattern = re.compile(r'арбитражный суд(.*?)(?:в составе|\n|$)')
    text = clear_newline_symbols(text)
    pattern = re.compile(r'(.*?арбитражный апелляционный суд)|(арбитражный суд.*?)(?:в составе|\n|$)')
    result = pattern.search(text).group(0) if pattern.search(text) else None

    res = {'span':None,'court':None}
    if pattern.search(text):
        span = pattern.search(text).span()
        result = result.strip()

        #cleared_court = clear_newline_symbols(result)

        res["span"] = span,
        #res["court"] =cleared_court,
        res['court'] = result
        

    return res

def find_parties(prepared_text):
    #Находим истца и ответчика
    pattern = re.compile(r'(?:заявлени[юяе]|иску)\s+(.*?)\s+[кК]\s+(.*?)\s+[оО]б?\s+(.*$)')
    matches = pattern.search(prepared_text)

    parties = {}

    plaintiff_w_inn = matches.group(1).strip() if matches else None

    parties['plaintiff_w_inn'] = plaintiff_w_inn
    if plaintiff_w_inn:
        extract_pattern = re.search(r'(.*?)(?:\(инн|\(огрн)', plaintiff_w_inn)

        if extract_pattern:
            plaintiff = extract_pattern.group(1).strip()
            parties['plaintiff'] = plaintiff
            parties['plaintiff_span'] = extract_pattern.span()

    defendant_w_inn = matches.group(2).strip() if matches else None

    parties['defendant_w_inn'] = defendant_w_inn
    if defendant_w_inn:
        extract_pattern = re.search(r'(.*?)(?:\(инн|\(огрн)', defendant_w_inn)

        if extract_pattern:
            defendant = extract_pattern.group(1).strip()
            parties['defendant'] = defendant
            parties['defendant_span'] = extract_pattern.span()


    rest_of_text = matches.group(3).strip() if matches else None


    return parties

def find_cause(text):
    #pattern = re.compile('[оО]б?\s+(.*$)')
    pattern = re.compile(' о (.*?)(?=при участии|представители|$)')
    result = pattern.findall(text)
    return result

def extract_inn(parties):
    # извлекаем инн-ы из строк истца и ответчика
    """
    TODO
    * Проверка на третье лицо
    """
    plaintiff = parties.get('plaintiff_w_inn')
    defendant = parties.get('defendant_w_inn')

    inns = []

    inn_pattern = re.compile(r'\b(\d{10}|\d{12})\b')
    plaintiff_inns = []
    defendant_inns = []

    if plaintiff:
        plaintiff_inns = inn_pattern.findall(plaintiff)
        for match in re.finditer(inn_pattern, plaintiff):
            if match:
                inn = {
                    "inn":match.group(1),
                    "span":(match.start(), match.end())
                }
                inns.append(inn)

    if defendant:    
        defendant_inns = inn_pattern.findall(defendant)
        for match in re.finditer(inn_pattern, defendant):
            if match:
                inn = {"inn":match.group(1), "span":(match.start(), match.end())}
                inns.append(inn)


    return {"plaintiff_inns":plaintiff_inns, "defendant_inns":defendant_inns, 'inns':inns}

def construct_result_json(example, court, parties, inns):
    return {
        "example":example,
        "court_entity" : (court.get('court'), court.get('span'), 'court'),
        "plaintiff_entity" : (parties.get('plaintiff_w_inn'), parties.get('plaintiff_span'), 'party'),
        "defendant_entity" : (parties.get('defendant_w_inn'), parties.get('defendant_span'),'party'),
        "inns" : inns['inns'],
    }

    #"court":court, "plaintiff":parties.get('plaintiff'),
    #"defendant":parties.get('defendant'), "plaintiff_inn":inns.get('plaintiff_inns'),
    #"defendant_inn":inns.get('defendant_inns'), #"resolution":resolution





def find_resolution(pdf):
    last_page_num = pdf.page_count

    last_page = pdf.load_page(last_page_num -1)
    text = last_page.get_text('text').lower()
    text = cleanup_text(text)
    text = clear_newline_symbols(text)

    regex_pattern = r'решил\s*:\s*(.*)'
    match = re.search(regex_pattern, text)

    if match:
        extracted_text = match.group(1)
        return extracted_text[:400]
    else:
        last_page = pdf.load_page(last_page_num -2)
        text =last_page.get_text('text').lower()
        text = cleanup_text(text)
        text = clear_newline_symbols(text)

        match = re.search(regex_pattern, text)
        if match:
            extracted_text = match.group(1)
            return extracted_text[:400]
    
result = {'result':[]}
for name in sorted(glob.glob('train_documents/*')):
    """
    TODO
    * Предобработка перед получением инн?
    * начало и конец дока
    * извлечение решения
    """
    result_json = {}

    print(f'doc:{name}')
    pdf = fitz.open(name)
    #resolution = find_resolution(pdf)

    page = pdf.load_page(0)
    line = page.get_text('text')[:2000]

    #line = extract_text(name)[:2000]
    line = cleanup_text(line).lower()
    line = clear_newline_symbols(line)
    print(line)
    print(find_cause(line))
    #print(line)
    court = find_court(line) if find_court(line) else print('Не найден суд')
    

    #delete newline symbols
    flattened_text = clear_newline_symbols(line)
    flattened_text = re.sub(r'\s+', ' ', flattened_text).strip()

    #print(flattened_text)
    parties = find_parties(flattened_text)

    inns = None
    inns = extract_inn(parties)
    #print(flattened_text)
    # pprint(construct_result_json(
    #         flattened_text,
    #         court,
    #         parties,
    #         inns,
    #         #resolution
    #     ))
    
    # result['result'].append(
    #     construct_result_json(
    #         flattened_text,
    #         court,
    #         parties,
    #         inns,
    #         #resolution
    #     ))

    



# with open('result.json','w',encoding='utf8') as res:
#     res.write(json.dumps(result,ensure_ascii=False))

# with open('result.json','r',encoding='utf8') as t:
#     pprint(json.load(t))
    


