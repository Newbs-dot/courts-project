# Модуль анализа текста судебных документов с источника kad.arbitr.ru
## Установка
- python -m venv .env
- source .env/bin/activate
- pip install -U pip setuptools wheel
- pip install -U spacy
- pip install pip-system-certs
- python -m spacy download ru_core_news_lg
- pip install PyMuPDF
- pip install fitz