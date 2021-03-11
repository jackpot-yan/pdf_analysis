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
        text = """<div id="page0" style="position:relative;width:595.3pt;height:841.9pt;background-color:white">""" + '\n\t' + """<p style="position:absolute;white-space:pre;margin:0;padding:0;top:78.25400000000002pt;left:90.0pt">"""
        result = self.info.generator_div_and_p_label()
        self.assertEqual(text, result)

    def test_span_label(self):
        text = """<div id="page0" style="position:relative;width:595.3pt;height:841.9pt;background-color:white">""" + '\n\t' + """<p style="position:absolute;white-space:pre;margin:0;padding:0;top:78.25400000000002pt;left:90.0pt"><span style="font-family:DroidSansFallback,serif;font-size:20.519999999999982pt">译</span></p>"""
        result = self.info.generator_text_html()
        self.assertEqual(text, result)

    def test_get_paragraph_length(self):
        text = 4
        result = self.info.get_current_paragraph_length()
        self.assertEqual(text, result)

    def test_generator_html(self):
        text = """<div id="page0" style="position:relative;width:595pt;height:841pt;background-color:white">
    <p style="position:absolute;white-space:pre;margin:0;padding:0;top:75pt;left:90pt"><span style="font-family:DroidSansFallback,serif;font-size:18pt">&#x8bd1;&#x8baf;&#x79d1;&#x6280;</span></p>
    <p style="position:absolute;white-space:pre;margin:0;padding:0;top:126pt;left:216pt"><span style="font-family:DroidSansFallback,serif;font-size:12pt">&#x7814;&#x53d1;&#x90e8;</span></p>
    <p style="position:absolute;white-space:pre;margin:0;padding:0;top:345pt;left:142pt"><span style="font-family:DroidSansFallback,serif;font-size:10.45pt">&#x8881;&#x6653;&#x5f64;</span></p>
</div>"""
        result = self.info.generator_text_html()
        self.assertEqual(text, result)

    def tearDown(self) -> None:
        self.data.close()
