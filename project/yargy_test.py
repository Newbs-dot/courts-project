# import os
# import re
# import json

# from yargy import Parser
# from yargy import rule
# from yargy.predicates import eq
# from yargy import or_, and_, not_
# from yargy import pipelines
# from yargy.interpretation import fact, attribute
# #from ipymarkup import show_markup

# Sud = fact( 'Sud', ['name', 'type'] )

# INT = type('INT') 
# LATIN = type('LATIN')
# DOT = eq('.') 
# DASH = eq('-')
from IPython.display import display
from yargy import ( Parser, rule, or_, not_, and_ ) 
from yargy.predicates import ( eq, type, caseless, in_, in_caseless, gte, lte, length_eq, is_capitalized, normalized, dictionary, gram, ) 
from yargy.pipelines import ( caseless_pipeline, morph_pipeline,pipeline ) 
from yargy.interpretation import ( fact, attribute )
from yargy import interpretation as interp 
from yargy.relations import gnc_relation
from yargy.tokenizer import ( QUOTES, LEFT_QUOTES, RIGHT_QUOTES, MorphTokenizer, TokenRule ) 
from ipymarkup import show_span_ascii_markup as show_markup
# CAPITALIZED = is_capitalized() 
# GEO = or_( rule(CAPITALIZED), rule( CAPITALIZED, DASH.optional(), CAPITALIZED ) ) 

# NUMERAL = rule(INT)
# NAME = or_( GEO, NUMERAL, ).interpretation( Sud.name.normalized() ) 

# MAIN_TYPE = morph_pipeline([ 
# 'dvd-диск', 'альманах','аудиовизуальный материал','аудиозапись', 'аудиокомпозиция', 
# 'аудиоматериал', 'аудиофайл', 'брошюра', 'вестник', 'видео-файл', 'видеозапись', 'видеоклип', 
# 'видеоматериал', 'видеообращение', 'видеоролик', 'видеофайл', 'видео файл', 'видеофильм', 'видеофонограмма', 
# 'визуальный материал', 'выпуск газеты', 'выпуск листовки', 'высказывания', 'газета', 'графическая работа', 
# 'графическое изображение', 'графический файл', 'демотиватор', 'документ', 'еженедельник', 'журнал', 'журнал-газета', 
# 'издание', 'изображение', 'информация', 'информационное видео', 'информационный материал', 'кинофильм', 'книга', 
# 'компьютерная игра', 'комментарий', 'листовка', 'лозунг', 'материал', 'музыкальный альбом', 'музыкальная композиция',
# 'музыкальное произведение', 'обозрение', 'печатное издание', 'печатный материал', 'печатная продукция', 'повесть', 
# 'программное обеспечение', 'произведение', 'прокламация', 'публикация', 'рисунок', 'статья', 'стихотворение', 'текст аудиозаписи',
# 'текст песни', 'текстово-графическое изображение', 'текстовый документ', 'текстовая информация',
# 'текстовая информация-статус', 'текстовое обращение', 'файл', 'фильм', 'фотография', 'фотоизображение', 
# 'электронный дневник', 'эссе', ]).interpretation( interp.normalized() )

# TYPE = dictionary({ 'федеральный', 'областной', 'городской', 'районный', 'гарнизонный', 'военный' }) 
# TYPE = or_( rule(TYPE), rule(TYPE, TYPE) ).interpretation( Sud.type.normalized() ) 
# SUD = rule( 
#     NAME.optional(),
#     TYPE.optional(), 
#     normalized('суд') ).interpretation( Sud )

# ITEM = rule( MAIN_TYPE.interpretation(Item.type), ATTRIBUTE.repeatable() ).interpretation( Item ) 

# FSEM = rule( ITEM.interpretation( Fsem.items ).repeatable(), DECISION.interpretation( Fsem.decision ) ).interpretation( Fsem )

INT = type('INT') 
COMMA = eq(',')
COLON = eq(':')

COURT_RULE= or_( 
    rule (
        normalized('Арбитражный'),
        normalized('суд'),
        gram('ADJF'),
        gram('NOUN')
        ),
    rule (
        normalized('Арбитражный'),
        normalized('суд'),
        gram('NOUN').optional().repeatable())
)

"""
TODO
Арбитраж
* г. - город
* обл. - область

сокращения
АО
ОАО
ООО
ОАОА МММ


Party
* по иску:
* по иску
* по заявлению
* заявление
* заявлени


"""

parser = Parser(COURT_RULE)
courts = '''
Арбитражного суда Республики Алтай
Арбитражный суд Алтайского края
Арбитражный суд Краснодарского края
АРБИТРАЖНЫЙ СУД Республики башкортостан
Арбитражный суд Свердловской Области
Арбитражный суд московской области
Арбитражный суд города москва
Арбитражный суд г. Москвы
'''
for match in parser.findall(courts):
    print([_.value for _ in match.tokens])
    #display(match.tree.as_dot)

QUOTE = in_(QUOTES) 
LEFT_QUOTE = in_(LEFT_QUOTES)
RIGHT_QUOTE = in_(RIGHT_QUOTES) 
QUOTED = or_( rule( LEFT_QUOTE, not_(RIGHT_QUOTE).repeatable(), RIGHT_QUOTE, ), 
            rule( and_( QUOTE, not_(RIGHT_QUOTE) ),
                  not_(QUOTE).repeatable(), 
                  and_( QUOTE, not_(LEFT_QUOTE) ) ) )
ANY_WORD = or_( rule(gram('NOUN').repeatable(),
        gram('ADJF').optional().repeatable(),
        gram('NOUN').repeatable()))
POSITION = or_(
    rule(
        normalized('заявление'), 
        COLON.optional(),
        ANY_WORD,
        normalized('к').optional(),
        normalized('о').optional(),
        normalized('об').optional(),
        gram('NOUN'),
    ),
    rule (
        normalized('иск'),
        COLON.optional(),
        gram('NOUN')).repeatable()

)



parser = Parser(POSITION)
zayavi = '''
ЗаяВлеНию орг1 к орг2
заявление: орг1 к Тандер
ЗаЯвЛеНиЕМ: орг1 к гАзпром
ЗаЯвЛеНиЕМ орг1 к хозпромсервис
ЗаЯвЛеНиЕМ орг1 о рога и копыта
ЗаЯвЛеНиЕМ орг1 К красный мак
ЗаЯвЛеНиЕМ орг1 Об мяу
по иску орг1 к пау-пау
по иску: по иску: бимбам к бумбум
по иску: бимбам К бумбум
иском: бимбам к бумбум
к производству искового заявления истца ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "МЕТАЛЛУРГИЧЕСКАЯ КОМПАНИЯ ЛОБНИ" (141733, РОССИЯ, МОСКОВСКАЯ ОБЛ., ЛОБНЯ Г.О., ЛОБНЯ Г., ЛОБНЯ Г., БУКИНСКОЕ Ш., Д. 4А, ОФИС 7, ОГРН: 1225000043542, Дата присвоения ОГРН: 05.05.2022, ИНН: 5047263290) к ответчику АКЦИОНЕРНОЕ ОБЩЕСТВО "РОССИЙСКИЙ СЕЛЬСКОХОЗЯЙСТВЕННЫЙ БАНК" (119034, Г МОСКВА, ГАГАРИНСКИЙ ПЕР, Д. 3, ОГРН: 1027700342890, Дата присвоения ОГРН: 22.10.2002, ИНН: 7725114488) об обязании совершить опер
заявлению УПРАВЛЕНИЯ ФЕДЕРАЛЬНОЙ СЛУЖБЫ ПО НАДЗОРУ В СФЕРЕ СВЯЗИ ИНФОРМАЦИОННЫХ ТЕХНОЛОГИЙ И МАССОВЫХ КОММУНИКАЦИЙ ПО ОМСКОЙ ОБЛАСТИ (644046, РОССИЯ, ОМСКАЯ ОБЛ., ГОРОД ОМСК Г.О., ОМСК Г., ОМСК Г., 4-Я ЛИНИЯ УЛ., Д. 178А, ОГРН: 1045504018570, Дата присвоения ОГРН: 23.07.2004, ИНН: 5503082200, КПП: 550601001) к заинтересованному лицу – ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "МОБИЛЬНЫЕ ТЕЛЕСИСТЕМЫ" (109147, ГОРОД МОСКВА, МАРКСИСТСКАЯ УЛИЦА, 4, ОГРН: 1027700149124, Дата присвоения ОГРН: 22.08.2002, ИНН: 7740000076, КПП: 770901001 об отмене Постановления от 19.01.2023 г. № 0356043010523011902000984) о привлечении к админи
Арбитражный суд Московской области в составе: судьи Бекетовой Е.А. при ведении протокола судебного заседания секретарем судебного заседания Старковой А.Ю., рассмотрев в судебном заседании дело по заявлению акционерного общества «МОСЭНЕРГОСБЫТ» (ИНН 7736520080, ОГРН 1057746557329) к врио начальника – старшего судебного пристава МО по ИОВИП №2 ГУФССП России по Московскй области Мкртчян А.А., судебному приставу – исполнителю МО по ИОВИП №2 ГУФССП России по Московской области Алханову Ш.К., ГУФССП России по Московской области о признании незаконным бездействия, третьи лица - Муниципальное унитарное предприятие городского округа Подольск «ДИРЕКЦИЯ ЕДИНОГО ЗАКАЗЧИКА» (ИНН 5036055450, ОГРН 1035007219301), при участии в судебном заседании: лиц согласно протоколу,
'''
for match in parser.findall(zayavi):
    print([_.value for _ in match.tokens])
    #display(match.tree.as_dot)


from yargy import not_ 
from yargy.predicates import eq
def bounded(start, stop): 
  return rule( eq(start), 
              not_(eq(stop)).repeatable(), 
              eq(stop) ) 

BOUNDED = or_( bounded('заявлению', 'о'), bounded('заявлению', 'к') ) 

parser = Parser(BOUNDED) 
matches = parser.findall('Арбитражный суд Московской области в составе: судьи Бекетовой Е.А. при ведении протокола судебного заседания секретарем судебного заседания Старковой А.Ю., рассмотрев в судебном заседании дело по заявлению акционерного общества «МОСЭНЕРГОСБЫТ» (ИНН 7736520080, ОГРН 1057746557329) к врио начальника – старшего судебного пристава МО по ИОВИП №2 ГУФССП России по Московскй области Мкртчян А.А., судебному приставу – исполнителю МО по ИОВИП №2 ГУФССП России по Московской области Алханову Ш.К., ГУФССП России по Московской области о признании незаконным бездействия, третьи лица - Муниципальное унитарное предприятие городского округа Подольск «ДИРЕКЦИЯ ЕДИНОГО ЗАКАЗЧИКА» (ИНН 5036055450, ОГРН 1035007219301), при участии в судебном заседании: лиц согласно протоколу,')
for match in matches: 
  print([_.value for _ in match.tokens])


def test_match(rule, *tests): 
  parser = Parser(rule) 
  for line in tests:
    for match in parser.findall(line):
      print([_.value for _ in match.tokens])

QUOTE = in_(QUOTES) 
LEFT_QUOTE = in_(LEFT_QUOTES)
RIGHT_QUOTE = in_(RIGHT_QUOTES) 
TITLE = or_( rule( LEFT_QUOTE, not_(RIGHT_QUOTE).repeatable(), RIGHT_QUOTE, ), 
            rule( and_( QUOTE, not_(RIGHT_QUOTE) ),
                  not_(QUOTE).repeatable(), 
                  and_( QUOTE, not_(LEFT_QUOTE) ) ) )

#print(test_match( TITLE, '«МЕТАЛЛУРГИЧЕСКАЯ КОМПАНИЯ ЛОБНИ»', '"Это должен знать Русский»', '"Правоохранительные органы РФ фальсифицируют факты и лживо обвиняют Хизб-ут-Тахрир аль-Ислами"'))


METRO_STATIONS = {'Проспект Мира',
  'Алма-Атинская',
  'Нахимовский проспект',
  'Парк Победы',
  'Проспект свободы',
  'Академгородок',
  'Достоевская',
  'Окружная',
  'Партизанская',
  'Козья слобода'}
AREAS = {'Старонижестеблиевская',
  'Голицыно',
  'Атаманская',
  'Перевальск',
  'Обоянь',
  'Кораблино',
  'Биробиджан',
  'Ижевск',
  'Чаплыгин',
  'Куйбышево'}

Intro = fact(
     'Intro', 
     ['gender', 'age', 'birth', 'location', attribute('citizenship').repeatable(),
       attribute('permission').repeatable(), 'relocation', 'travel', 'position', 
       attribute('subspecializations').repeatable(), 'employment', 'schedule', 'commute', 'salary' ] ) 

def show_matches(rule, *lines):
    parser = Parser(rule)
    for line in lines: 
        matches = parser.findall(line)
        spans = [_.span for _ in matches] 
        show_markup(line, spans)

Court = fact( 'Court', ['name'] ) 
TITLE = rule(caseless('Арбитражный суд'),
             gram('NOUN').optional().repeatable()) 

Location = fact( 'Location', ['area', 'metro'] ) 

METRO = rule( 'м', '.', pipeline(METRO_STATIONS).interpretation( Location.metro ) ) 
AREA = pipeline(AREAS).interpretation( Location.area )
LOCATION = rule( AREA, rule( COMMA, METRO ).optional() ).interpretation( Location )
#show_matches( LOCATION, 'место проживания: Москва, м. Парк Победы', 'Киев, м.Киевская', 'Россия', 'в Москве', 'м. парк победы', 'на м. Кропоткинской', )

TITLE = rule(caseless('Арбитражный суд')) 
ITEM = AREA.interpretation( Intro.citizenship ) 
LOCATIONS = rule( ITEM, rule( COMMA, ITEM ).optional() )
CITIZENSHIP = rule( TITLE, LOCATIONS ) 
#show_matches( CITIZENSHIP, 'Гражданство: Россия, Франция', 'Гражданство: Россия, Франция, Украина', )

TITLE = pipeline([ 'есть разрешение на работу:' ]) 
ITEM = AREA.interpretation( Intro.permission ) 
LOCATIONS = rule( ITEM, rule( COMMA, ITEM ).optional().repeatable() ) 
PERMISSION = rule( TITLE, LOCATIONS ) 
#show_matches( PERMISSION, 'есть разрешение на работу: Россия, Франция, Украина', 'есть разрешение на работу: Россия', )



    