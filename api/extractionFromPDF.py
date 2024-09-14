#!/usr/bin/env python
# coding: utf-8

# In[9]:


import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from img2table.document import Image 
from img2table.ocr import PaddleOCR
import importlib
import PIL
importlib.reload(PIL)
import io
from PIL import Image as PILImage 
from IPython.display import display_html

pdf_path = r"C:\Users\meghana.m\Desktop\SPIS\ALL PDFs\225592 UNIVERSITY OF KENTUCKY MED CTR.pdf"
poppler_bin_path= r"C:\Users\meghana.m\Downloads\poppler-23.08.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\meghana.m\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pages = convert_from_path(pdf_path, 300, poppler_path=poppler_bin_path)

ocr = PaddleOCR(lang="en",
                kw={"use_dilation": True})

def text_extraction(page, page_num):
    
    with io.BytesIO() as byte_stream:
        page.save(byte_stream, format="PPM")
        byte_stream.seek(0)
        img = Image(src=byte_stream)
        tables = img.extract_tables(ocr=ocr, borderless_tables=True)

        for idx, table in enumerate(tables):
            display_html(table.html_repr(title=f"Extracted table n°{idx + 1}"), raw=True)

        image_data = page.convert('RGB')

        if tables:
            for table in tables:
                x1, y1, x2, y2 = table.bbox.x1, table.bbox.y1, table.bbox.x2, table.bbox.y2
                mask = PILImage.new('RGB', (x2 - x1, y2 - y1), color=(255, 255, 255))  
                image_data.paste(mask, (x1, y1))  

        text = pytesseract.image_to_string(image_data, config='--psm 6')
        print(text)

page_num=0
for page in pages:
    page_num+=1
    text_extraction(page, page_num)

