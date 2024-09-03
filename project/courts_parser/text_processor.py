import re


class TextProcessor:
    """Класс для обработки текста"""
    @classmethod
    def _clear_newline_symbols(self, text):
        return text.replace('\n', ' ') if text else ''
    
    @classmethod
    def _cleanup_excess_spaces(self, text):
        excess_whitespaces = re.sub(r'[ \t]+', ' ', text)
        return excess_whitespaces

    @classmethod
    def clear_text(cls, text) -> str:
        text = cls._clear_newline_symbols(text)
        text = cls._cleanup_excess_spaces(text)
        return text
