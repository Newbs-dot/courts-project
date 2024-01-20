import glob
import re
import fitz
from pdfminer.high_level import extract_pages, extract_text
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
    pattern = re.compile(r'(.*?арбитражный апелляционный суд)|(арбитражный суд.*?)(?:в составе|\n|$)')
    result = pattern.search(text).group(0) if pattern.search(text) else None
    return result

def find_parties(prepared_text):
    #Находим истца и ответчика
    pattern = re.compile(r'(?:заявлению|иску|заявления|заявление)\s+(.*?)\s+[кК]\s+(.*?)\s+[оО]б?\s+(.*$)')
    matches = pattern.search(prepared_text)

    plaintiff = matches.group(1).strip() if matches else None
    defendant = matches.group(2).strip() if matches else None
    rest_of_text = matches.group(3).strip() if matches else None
    
    return plaintiff,defendant

def extract_inn(parties):
    # извлекаем инн-ы из строк истца и ответчика
    """
    TODO
    * Проверка на третье лицо
    """
    plaintiff,defendant = parties
    inn_pattern = re.compile(r'\b(\d{10}|\d{12})\b')
    plaintiff_inns = inn_pattern.findall(plaintiff) if plaintiff else None
    defendant_inns = inn_pattern.findall(defendant) if defendant else None

    return {"plaintiff_inns":plaintiff_inns, "defendant_inns":defendant_inns}

def construct_result_json(court,parties,inns,resolution):
    return json.dumps(
        {
            "court":court,
            "plaintiff":parties.popleft(),
            "defendant":parties.pop(),
            "plaintiff_inn":inns.get('plaintiff_inns'),
            "defendant_inn":inns.get('defendant_inns'),
            "resolution":resolution
        })

def clear_newline_symbols(text):
    return text.replace('\n', '') if text else ''

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
    

for name in sorted(glob.glob('documents/*')):
    """
    TODO
    * Предобработка перед получением инн?
    * начало и конец дока
    * извлечение решения
    """
    result_json = {}

    print(f'doc:{name}')
    pdf = fitz.open(name)
    resolution = find_resolution(pdf)

    page = pdf.load_page(0)
    line = page.get_text('text')[:2000]

    #line = extract_text(name)[:2000]
    line = cleanup_text(line).lower()
    #print(line)
    court = find_court(line) if find_court(line) else print('Не найден суд')
    cleared_court = clear_newline_symbols(court)

    #delete newline symbols
    flattened_text = clear_newline_symbols(line)
    flattened_text = re.sub(r'\s+', ' ', flattened_text).strip()

    #print(flattened_text)
    parties = deque(find_parties(flattened_text))

    inns = None
    inns = extract_inn(parties)

    result = json.loads(construct_result_json(
        cleared_court,
        parties,
        inns,
        resolution
        ))
    
    pprint(result)
    
    #pprint(result)
    


