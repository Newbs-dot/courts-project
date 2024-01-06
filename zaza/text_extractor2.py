from pdfminer.high_level import extract_pages, extract_text

for page_layout in extract_pages('example3.pdf'):
    for element in page_layout:
        #print(element)
        pass

import re
import fitz

pdf = fitz.open('example.pdf')

page = pdf.load_page(0)
text = page.get_text('text')
text = text.lower()
pdf.close()


pattern = re.compile(r'арбитражный суд[^\n]*')

# Find matches in the text
matches = pattern.search(text)

# Extract matched part
extracted_text = matches.group() if matches else None

# Print the results
print("Extracted Text:")
print(extracted_text)