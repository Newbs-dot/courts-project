import re

class RegexExtractor:

    def __init__(self) -> None:
        pass

    @staticmethod
    def find_cause(text):
        #интелелктуальной о запрете
        pattern = r'о (взыскании|вынесении|признании|обязании|привлечении)(.*?)(при участии|представители|третье лицо|лица|руководствуясь|установил)'
        match = re.search(pattern,text, re.IGNORECASE)
        return match.group(2) if match else None
    
    @staticmethod
    def find_case(text):
        pattern = r'дело №\s*(.*?)(?:$|\s)'
        match = re.search(pattern,text, re.IGNORECASE)
        return match.group(1) if match else None
    
    @staticmethod
    def find_court(text):
        #TODO Интеллектуальный итд
        pattern = re.compile(r'Арбитражный суд\s+(.*?)(?=в составе|$)', re.IGNORECASE)
        match = re.search(pattern,text)
        return match.group(1) if match else None

