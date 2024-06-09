from PIL import Image
import fitz
import tqdm
import pytesseract
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


doc = fitz.Document('D:\диплом\courts-project\project\pdf_with_img.pdf')

for i in range(len(doc)):
    for img in doc.get_page_images(i):
        xref = img[0]
        image = doc.extract_image(xref)
        pix = fitz.Pixmap(doc, xref)
        img_bytes = pix.tobytes()
        print(pytesseract.image_to_string(Image.open(io.BytesIO(img_bytes)), lang='rus'))
        
                
