import glob
import re
import fitz
from pdfminer.high_level import extract_pages, extract_text

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




for name in sorted(glob.glob('documents/*')):
    """
    TODO
    * Предобработка перед получением инн?
    """
    print(f'doc:{name}')
    pdf = fitz.open(name)

    page = pdf.load_page(0)
    line = page.get_text('text')[:2000]

    #line = extract_text(name)[:2000]
    line = cleanup_text(line).lower()

    court = find_court(line) if find_court(line) else print('Не найден суд')

    flattened_text = line.replace('\n', '')
    flattened_text = re.sub(r'\s+', ' ', flattened_text).strip()

    #print(flattened_text)
    parties = find_parties(flattened_text)

    inns = None
    inns = extract_inn(parties)

    print(f"""
        СУД {court}
        Истец {parties[0]}
        Ответчик {parties[1]}
        ИНН исца {inns.get('plaintiff_inns')}
        ИНН ответчика {inns.get('defendant_inns')}""")

