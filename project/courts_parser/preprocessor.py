import re

class Preprocessor:

    def __init__(self) -> None:
        pass
    
    def _clear_newline_symbols(self, text):
        return text.replace('\n', '') if text else ''
    
    def _cleanup_excess_spaces(self, text):
    #Очищаем текст от лишних пробелов внутри слов и между ними
        whitespaces_between_characters = re.sub(r'(?<=\b\w)\s(?=\w\b)','', text)
        excess_whitespaces = re.sub(r'[ \t]+', ' ', whitespaces_between_characters)
        return excess_whitespaces

    def clear_text(self, text) -> str:
        text = self._clear_newline_symbols(text)
        text = self._cleanup_excess_spaces(text)
        return text