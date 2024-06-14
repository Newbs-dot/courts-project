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
    
    # @classmethod
    # def clear_result(cls,text):
    #     if text:
    #         text = text.replace('"','')
    #         text = text.replace('руб.','')
    #         text = text.replace('общество с ограниченной ответственностью','ООО')
    #         text = text.replace('Арбитражный суд','АС')
    #         return text.strip()