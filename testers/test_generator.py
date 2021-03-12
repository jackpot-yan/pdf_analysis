from unittest import TestCase
from generator_file import *
from testers import test_pdf


class Tester(TestCase):
    def setUp(self) -> None:
        self.data = open(test_pdf, 'rb')
        pdf_reader = PDFReader(self.data)
        pdf_pages = pdf_reader.get_pages_generator()
        self.page = next(pdf_pages)
        self.text_reader = TextReader(self.page)
        self.info = Generator(self.page)

    def test_div_label(self):
        text = """<div style="position:relative;width:595.3pt;height:841.9pt;">"""
        result = self.info.generator_div_label()
        self.assertEqual(text, result)

    def test_span_label(self):
        text = ('<p style="position:absolute; padding:78.25400000000002pt 90.0pt">', 4)
        result = next(self.info.generator_p_label())
        self.assertEqual(text, result)

    def test_get_paragraph_length(self):
        text = 4
        result = self.info.get_current_paragraph_length()
        self.assertEqual(text, result)

    def test_generator_html(self):
        text = 25444
        result = self.info.generator_html_file()
        self.assertEqual(text, result)

    def tearDown(self) -> None:
        self.data.close()
