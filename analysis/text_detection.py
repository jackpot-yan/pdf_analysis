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

    def set_coordination_in_page(self, coordination):
        self.size = coordination
        return self.size

    # def set_eson_box(self, box):
    #     box = self.bbox
    #     return box

    # def get_box(self):
    #     box = self.mediabox
    #     return box

    # @property
    # def left_up(self):
    #     return True
    #
    # @property
    # def right_up(self):
    #     return None
    #
    # @property
    # def left_down(self):
    #     return None
    #
    # @property
    # def right_down(self):
    #     return None


class EsonPDFTextLine(LTTextLine):

    def __init__(self):
        super(EsonPDFTextLine, self).__init__()

    def set_eson_box(self, box):
        self.text_box = box


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
        # temp = list(filter(lambda x: isinstance(x, LTChar), text_line))
        # temp2 = [EsonPDFChar(x) for x in temp]
        # temp3 = [x.set_coordination_in_page(_x, _y) for x in temp2]
        # return temp3

    @staticmethod
    def convert_LTChar2EsonChar(lt_char):
        lt_char.__class__ = EsonPDFChar
        # lt_char.set_eson_box(lt_box)
        return lt_char

    @staticmethod
    def convert_LTTextLine2EsonTextLine(lt_line, lt_box):
        lt_line.__class__ = EsonPDFTextLine
        lt_line.set_eson_box(lt_box)

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
        self.page = EsonPDFPage(page)
        self.page_size = self.page.page_size

    def get_text_box_info(self, text_box):
        paragraph = {}
        x, y, content = text_box.bbox[0], self.page_size['height'] - text_box.bbox[3], text_box.get_text()
        paragraph[content] = [x, y]
        return paragraph

    def get_char_info(self, chars):
        font_style = []
        text, text_size, font_name = chars.get_text(), chars.size, chars.fontname
        text_x, text_y = chars.bbox[0], self.page_size['height'] - chars.bbox[3]
        font_list = [text, text_size, font_name, text_x, text_y]
        font_style.append(font_list)
        return font_style
