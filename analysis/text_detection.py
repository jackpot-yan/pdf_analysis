from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LTTextBox, LTTextLine, LTChar, LTFigure
from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument
from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
import os

path = '/home/jackpot/PycharmProjects/pdf_analysis/002-英译中PDF+.pdf'


class TextExtraction:
    def __init__(self, file_path, out_file_path):
        self.file_path = file_path
        self.out_file_path = out_file_path

    def get_file_data(self):
        file_data = open(self.file_path, 'rb')
        return file_data

    def get_parser(self):
        parser = PDFParser(TextExtraction.get_parser(self))
        return parser
