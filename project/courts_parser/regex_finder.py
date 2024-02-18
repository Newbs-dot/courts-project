import re

class RegexFinder:

    def __init__(self) -> None:
        pass

    def find_case_num(self, text):
        case_pattern = re.compile(r'Дело № ([^\s]+)')
        match = re.search(case_pattern, text)
        return match.group(1)
    
#finder = RegexFinder()
#print(finder.find_case_num('Дело № А-123/1231 Арбиатжный суд'))
