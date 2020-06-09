
@author Nawwar Mokayes

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


def convert_pdf_into_txt(pdf_file_path):
    pdf_resource_manager = PDFResourceManager()
    string_manager = StringIO()
    codec = 'utf-8'
    laparams = LAParams()

    converter = TextConverter(pdf_resource_manager, string_manager, codec=codec, laparams=laparams)

    pdf_file_data = file(pdf_file_path, 'rb')
    interpreter = PDFPageInterpreter(pdf_resource_manager, converter)

    # in case the pdf is protected with a password
    password = ""

    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(pdf_file_data, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = string_manager.getvalue()

    text = text.replace('\r\n', '')
    text = text.replace('\n', '')

    pdf_file_data.close()
    converter.close()
    string_manager.close()
    return text
