from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LTTextBox, LTTextLine, LTChar, LTFigure
from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument
from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.layout import LAParams
from io import StringIO
from io import open
import os

path = '/testers/test_files/test.pdf'


class File:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def get_file_data(self):
        file_data = open(self.input_file, 'rb')
        return file_data

    def close_file(self):
        self.get_file_data().close()
        return True

    def write_to_file(self, content):
        with open(self.output_file, 'w+') as file:
            file.write(content)


class PDFReader:
    def __init__(self, pdf_data):
        self.pdf_parser = PDFParser(pdf_data)
        self.pdf_document = PDFDocument()
        self.pdf_parser.set_document(self.pdf_document)
        self.pdf_document.set_parser(self.pdf_parser)

    def get_pages_generator(self):
        return self.pdf_document.get_pages()

    def get_page_count(self):
        pages = self.get_pages_generator()
        return self.get_len_of_generator(pages)

    @staticmethod
    def get_len_of_generator(generator):
        length = 0
        for _ in generator:
            length += 1
        return length


class TextReader:
    def __init__(self, page):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        self.device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        self.interpreter = PDFPageInterpreter(rsrcmgr, self.device)
        self.page = page

    def get_layout(self):
        self.interpreter.process_page(self.page)
        return self.device.get_result()

    def get_all_text_box(self):
        return list(filter(lambda x: isinstance(x, LTTextBox) or isinstance(x, LTFigure), self.get_layout()))

    def get_all_text_line(self):
        pass
