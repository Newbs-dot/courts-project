import re
from pprint import pprint
import glob
import fitz
import json
from pdfminer.high_level import extract_text, extract_pages



def clear_newline_symbols(text):
    return text.replace('\n', '') if text else ''

def cleanup_text(text):
    #Очищаем текст от лишних пробелов внутри слов и между ними
    whitespaces_between_characters = re.sub(r'(?<=\b\w)\s(?=\w\b)','', text)
    excess_whitespaces = re.sub(r'[ \t]+', ' ', whitespaces_between_characters)
    return excess_whitespaces

def find_cause(text):
    #интелелктуальной о запрете
    pattern = r'о (взыскании|вынесении|признании|обязании|привлечении)(.*?)(при участии|представители|третье лицо|лица|руководствуясь|установил)'
    match = re.search(pattern,text, re.IGNORECASE)
    return match.group(2) if match else None

for name in sorted(glob.glob('test_documents/*')):
    print(f'doc:{name}')
    pdf = fitz.open(name)
    page = pdf.load_page(0)
    output = page.get_text("text")
    print(output)
    output = clear_newline_symbols(output)
    
    
    print(name, find_cause(output))