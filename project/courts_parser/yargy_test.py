from yargy import not_ 
from yargy.predicates import eq
from yargy import ( Parser, rule, or_, not_, and_ ) 
from fuzzywuzzy import fuzz

def bounded(start, stop): 
    return rule( eq(start), not_(eq(stop)).repeatable(), eq(stop) ) 

BOUNDED = or_( bounded('(',')') ) 

parser = Parser(BOUNDED) 
matches = parser.findall('(ИНН 6606022606, ОГРН 1069606006953) г. Верхняя Пышма Свердловской области')
for match in matches: 
  print([_.value for _ in match.tokens])

s1 = 'индивидуальному предпринимателю Охват Оксане Владимировне'
s2 = 'индивидуальный предприниматель Охват Оксана Владимировна'
s3 = 'общества с ограниченной ответственностью «УГМК-Телеком»'

print(fuzz.ratio(s1,s2))

from difflib import SequenceMatcher
# Яблоко, только под разными названиями..

similarity_ratio = SequenceMatcher(None, s1,s2).ratio()
print(similarity_ratio)

