import re

def extract_arbitrazh_sud_phrases(text):
    # Define regex pattern to extract phrases starting from 'Арбитражный суд' until 'в составе' or newline
    pattern = re.compile(r'арбитражный суд(.*?)(?:в составе|\n|$)')

    # Find all matches in the text
    matches = pattern.findall(text)

    return matches

# Example usage
input_text = '''
Арбитражный суд республики Дагестан
г. Махачкала
9 июня 2021 года Дело №А15-1627/2020
Резолютивная часть решения объявлена 2 июня 2021 года
Мотивированное решение изготовлено 9 июня 2021 года
Арбитражный суд Республики Дагестан в составе судьи Ахмедовой Г.М.,
при ведении протокола судебного заседания секретарем Меджидовым P.P.,
рассмотрев в открытом судебном заседании материалы дела по иску
ЗАО «Каспий-1» в лице акционера ПАО «НК «Роснефть-Дагнефть»
к АО «Россельхозбанк (Дагестанский филиал)
о признании недействительными договоров поручительства №100400/0001-8 от 20.01.2010
и №140400/0047 от 16.10.2014,
'''

result = extract_arbitrazh_sud_phrases(input_text.lower())

print("Original Text:")
print(input_text)

print("\nExtracted Phrases:")
print(result)

import re

def extract_arbitrazh_appeal_suds(text):
    # Define regex pattern to extract phrases with numbers before 'арбитражный аппеляционный суд'
    #pattern = re.compile(r'.*?арбитражный аппеляционный суд')
    pattern = re.compile(r'(.*?арбитражный аппеляционный суд)|(арбитражный суд.*?)(?:в составе|\n|$)')
    # Find all matches in the text
    matches = pattern.findall(text)

    return matches

# Example usage
input_text = """
ДЕВЯТЫЙ АРБИТРАЖНЫЙ АПЕЛЛЯЦИОННЫЙ СУД
127994, Москва, ГСП-4, проезд Соломенной cторожки, 12
адрес электронной почты: info@mail.9aac.ru
адрес веб.сайта: http://www.9aas.arbitr.ru
ОПРЕДЕЛЕНИЕ
о принятии апелляционной жалобы к производству
"""

result = extract_arbitrazh_appeal_suds(input_text.lower())

print("Original Text:")
print(input_text)

print("\nExtracted Phrases:")
for phrase in result:
    print(phrase)



test = 'org2: открытому акционерному обществу "Уральская горно-металлургическая компания" (ИНН: 6606013640, ОГРН: 1026600727713) третье лицо: 660601364111'
entities = re.compile(r'\b(\d{10}|\d{12})\b')  
matches = entities.findall(test)
plaintiff,defendant = matches


print(defendant)