import pymorphy3

# Create a morphological analyzer
morph = pymorphy3.MorphAnalyzer()

phrase = 'обществу с ограниченной ответственностью'
phrase3 = 'общества с ограниченной ответственностью угмк-телеком'
phrase4 = 'индивидуальному предпринимателю Охват Оксане Владимировне'
phrase5 = 'Акционерного общества "Тулагорводоканал"'
phrase6 = 'Акционерному обществу "Тандер"'
phrase2 = 'Федерального государственного унитарного предприятия Охрана'
phrase7 = 'Управления Федеральной службы по надзору в сфере связи, информационных технологий и массовых коммуникаций по Республике Бурятия'
phrase8 = 'публичному акционерному обществу «Мобильные телесистемы»'

for p in phrase8.split(' '):
    try:
        parsed_phrase = morph.parse(p)[0]
        if 'neut' in parsed_phrase.tag or 'datv' in parsed_phrase.tag and not 'masc' in parsed_phrase.tag:
            parsed_phrase = parsed_phrase.inflect({'nomn'})
        
        print(parsed_phrase.word)
    except:
        pass
    

#check form
# parsed_phrase = morph.parse('обществу')[0].inflect({'sing', 'nomn'}).word
# print(parsed_phrase)

