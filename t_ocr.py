POPPLER_PATH = r"L:\Program Files\poppler\Library\bin"

from sys import argv
from re import sub

import pdf2image
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


def pdf_to_img(pdf_file):
    return pdf2image.convert_from_path(pdf_file, poppler_path = POPPLER_PATH)


def ocr_core(file, lang):
    text = pytesseract.image_to_string(file, lang)
    return text


def ocr_pages(pdf_file, lang):
    images = pdf_to_img(pdf_file)
    text=''
    for pg, img in enumerate(images):
        text+=ocr_core(img, lang)
    return text

if len(argv)<2:
    print('''Usage:
    ocr.py <filename> [<lang>]
    lang in format for Tesseract, more then one languages with +
    Text goes to output.
    ''')
    exit()

filename=argv[1]
lang = argv[2] if len(argv)>2 else 'eng'
if filename[-4:]=='.pdf':
    text = ocr_pages(filename, lang)
else:
    text = ocr_core(Image.open(filename), lang)
print(sub(r'—\n','— ',
      sub(r'-\n','',
      sub(r',\n',', ',
      sub(r';\n','; ',
      sub(r'([a-z])\n',r'\1 ',
      sub(r'([á-ž])\n',r'\1 ',
      text.replace(
      '<','«').replace('>','»')
)))))))