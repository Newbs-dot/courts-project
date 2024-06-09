from PIL import Image

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class TesseractExtractor:
    """Класс для извлечения данных с помощью OCR (Tesseract)"""
    
    def __init__(self, main_model_path, sums_model_path) -> None:
        self.model_path = main_model_path
        self.sums_model_path = sums_model_path
        self.sums_doc = None
        self.general_info_doc = None

    def extract_images(self,doc_path):

        doc = fitz.Document('D:\диплом\courts-project\project\pdf_with_img.pdf')

        for i in range(len(doc)):
            for img in doc.get_page_images(i):
                xref = img[0]
                image = doc.extract_image(xref)
                pix = fitz.Pixmap(doc, xref)
                img_bytes = pix.tobytes()
                print(pytesseract.image_to_string(Image.open(io.BytesIO(img_bytes)), lang='rus'))