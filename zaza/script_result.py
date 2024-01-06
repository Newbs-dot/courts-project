import glob
import re
import fitz
from pdfminer.high_level import extract_pages, extract_text

"""
1)есть название судов через перенос строки
2)вот такое А Р Б И Т Р А Ж Н Ы Й С У Д
3)в виде изображения
4)еще номерной аппеляционный
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
    whitespaces_between_characters = re.sub(r'(?<=\b\w)\s(?=\w\b)','', text)
    excess_whitespaces = re.sub(r'[ \t]+', ' ', whitespaces_between_characters)
    return excess_whitespaces

def find_court(text):
    #pattern = re.compile(r'арбитражный суд(.*?)(?:в составе|\n|$)')
    pattern = re.compile(r'(.*?арбитражный апелляционный суд)|(арбитражный суд.*?)(?:в составе|\n|$)')
    result = pattern.search(text).group(0) if pattern.search(text) else None
    return result

for name in sorted(glob.glob('documents/*')):
    print(f'doc:{name}')
    #брать не 500, а сначала убрать лишние пробелы
    line = extract_text(name)[:500]
    line = cleanup_text(line).lower()
    court = find_court(line) if find_court(line) else print('Не найден суд')
    print(court)

