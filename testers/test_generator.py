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
        text = """<div id="page0" style="position:relative;width:595.3pt;height:841.9pt;background-color:white">"""
        result = self.info.generator_div_label()
        self.assertEqual(text, result)

    def test_p_div_label(self):
        lt_box = self.text_reader.get_all_text_box()[0]
        text = """<div id="page0" style="position:relative;width:595.3pt;height:841.9pt;background-color:white">""" + '\n\t' + """<p style="position:absolute;white-space:pre;margin:0;padding:0;top:78.25400000000002pt;left:90.0pt">"""
        result = self.info.generator_div_and_p_label(lt_box)
        self.assertEqual(text, result)

    def test_span_label(self):
        lt_char = self.text_reader.get_all_text_char()[0]
        text = """<div id="page0" style="position:relative;width:595pt;height:841pt;background-color:white">""" + '\n\t' + """<p style="position:absolute;white-space:pre;margin:0;padding:0;top:75pt;left:90pt"><span style="font-family:HYUHQC+DroidSansFallback,serif;font-size:20.519999999999982pt">译</span></p>"""
        result = self.info.generator_text_html(lt_char)
        self.assertEqual(text, result)

    def tearDown(self) -> None:
        self.data.close()
