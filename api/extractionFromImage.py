#!/usr/bin/env python
# coding: utf-8

# In[78]:


from img2table.document import Image
from img2table.ocr import PaddleOCR
from IPython.display import display_html
from PIL import Image as PILImage 
import time
import pytesseract
start=time.time()
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\meghana.m\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

original_img = PILImage.open(r'C:\Users\meghana.m\Desktop\SPIS\Table img\images-0 (29).jpg')

img = Image(r'C:\Users\meghana.m\Desktop\SPIS\Table img\images-0 (29).jpg', 
              detect_rotation=True)

paddle_ocr = PaddleOCR(lang="en", kw={"use_dilation": True})

extracted_tables = img.extract_tables(ocr=paddle_ocr)

for idx, table in enumerate(extracted_tables):
    display_html(table.html_repr(title=f"Extracted table n°{idx + 1}"), raw=True)

if extracted_tables:
    for table in extracted_tables:
        x1, y1, x2, y2 = table.bbox.x1, table.bbox.y1, table.bbox.x2, table.bbox.y2
        
        mask = PILImage.new('RGB', (x2 - x1, y2 - y1), color=(255, 255, 255))
        
        original_img.paste(mask, (x1, y1))

text = pytesseract.image_to_string(original_img, config='--psm 6')

text_lines = []  

for line in text.splitlines():  
    if line.strip():  
        text_lines.append(line.strip())

for i in text_lines:
    print(i)

end=time.time()

total_time=end-start

print(total_time)

