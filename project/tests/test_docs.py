#open pdf
#preprocess
#test
import re

#assert@staticmethod
def find_court(text):
    #TODO Интеллектуальный итд
    pattern = re.compile(r'Арбитражный суд\s+(.*?)(?=в составе|$)')
    match = re.search(pattern,text)
    return match.group(0) if match else None
text = """
АРБИТРАЖНЫЙ СУД АЛТАЙСКОГО КРАЯ 656015, Барнаул, пр. Ленина, д. 76,тел (3852) 29-88-01 http:// www.altai-krai.arbitr.ru, е mail:а03.info@arbitr.ru Именем Российской Федерации Резолютивная часть решения арбитражного суда по делу, рассмотренному в порядке упрощенного производства г. Барнаул Дело № А03-3155/2020 29 апреля 2020 год Арбитражный суд Алтайского края в составе судьи

"""
print(find_court(text))