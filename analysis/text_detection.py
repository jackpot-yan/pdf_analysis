from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LTTextBox, LTTextLine, LTChar, LTFigure, LTTextBoxHorizontal, LTPage
from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument, PDFPage
from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.layout import LAParams
from io import StringIO
from io import open
import os

#  pdfminer官方文档 https://pdfminersix.readthedocs.io/

path = '/testers/test_files/test.pdf'


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


class EsonPDFChar(LTChar):
    def set_coordination_in_page(self, page_config):
        Eson_coordination = page_config['height'] - self.bbox[3]
        return Eson_coordination


class EsonPDFTextBox(LTTextBox):
    def set_coordination_in_page(self, page_config):
        y2 = page_config['height'] - self.bbox[3]
        return y2

    @property
    def get_len_text_box(self):
        len_box = len(self.get_text().replace('\n', '').replace(' ', ''))
        return len_box


class TextReader:
    def __init__(self, page):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        self.device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        self.interpreter = PDFPageInterpreter(rsrcmgr, self.device)
        self.page = page

    @staticmethod
    def get_text_line_from_text_box(text_box):
        return list(filter(lambda x: isinstance(x, LTTextLine), text_box))

    @staticmethod
    def get_text_char_from_text_line(text_line):
        return list(filter(lambda x: isinstance(x, LTChar), text_line))

    @staticmethod
    def convert_LTTextBox2EsonBox(lt_box):
        lt_box.__class__ = EsonPDFTextBox
        return lt_box

    @staticmethod
    def convert_LTChar2EsonChar(lt_char):
        lt_char.__class__ = EsonPDFChar
        return lt_char

    def get_layout(self):
        self.interpreter.process_page(self.page)
        return self.device.get_result()

    def get_all_text_box(self):
        return list(filter(lambda x: isinstance(x, LTTextBox), self.get_layout()))

    def get_all_text_line(self):
        rtn = []
        for box in self.get_all_text_box():
            rtn.extend(self.get_text_line_from_text_box(box))
        return rtn

    def get_all_text_char(self):
        rtn = []
        for line in self.get_all_text_line():
            rtn.extend(self.get_text_char_from_text_line(line))
        return rtn

    def get_page_size(self):
        config = {'width': self.page.mediabox[2], 'height': self.page.mediabox[3]}
        return config


class EsonPDFPage:
    def __init__(self, page):
        self.page = page
        self.text_reader = TextReader(page)

    @property
    def page_size(self):
        return {'width': self.page.mediabox[2], 'height': self.page.mediabox[3]}

    @property
    def all_text_box(self):
        return self.text_reader.get_all_text_box()

    @property
    def all_text_line(self):
        return self.text_reader.get_all_text_line()

    @property
    def all_text_char(self):
        return self.text_reader.get_all_text_char()


class PDFObjectInfo:
    def __init__(self, page):
        self.page = TextReader(page)
        self.page_size = self.page.get_page_size()

    def get_all_text_box_info(self):
        paragraph = {}
        lt_boxes = self.page.get_all_text_box()
        for lt_box in lt_boxes:
            lt_box.__class__ = EsonPDFTextBox
            x, y, content, length = lt_box.bbox[0], lt_box.set_coordination_in_page(self.page_size), lt_box.get_text(), lt_box.get_len_text_box
            paragraph[content] = [x, y, length]
        return paragraph

    def get_all_char_info(self):
        font_style = []
        lt_chars = self.page.get_all_text_char()
        for char in lt_chars:
            char.__class__ = EsonPDFChar
            text, text_size, font_name = char.get_text(), char.size, char.fontname
            if ' ' in text or '\n' in text:
                continue
            text_x, text_y = char.bbox[0], char.set_coordination_in_page(self.page_size)
            font_list = [text, text_size, font_name, text_x, text_y]
            font_style.append(font_list)
        return font_style
