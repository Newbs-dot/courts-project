import re

class Preprocessor:
    """Класс для предобработки текста"""
    def __init__(self) -> None:
        pass
    
    def _clear_newline_symbols(self, text):
        return text.replace('\n', ' ') if text else ''
    
    def _cleanup_excess_spaces(self, text):
        excess_whitespaces = re.sub(r'[ \t]+', ' ', text)
        return excess_whitespaces

    def clear_text(self, text) -> str:
        text = self._clear_newline_symbols(text)
        text = self._cleanup_excess_spaces(text)
        return text