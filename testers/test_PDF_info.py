from unittest import TestCase
from analysis.text_detection import *
from testers import test_pdf


class Tester(TestCase):
    def setUp(self) -> None:
        self.data = open(test_pdf, 'rb')
        pdf_reader = PDFReader(self.data)
        pages_generator = pdf_reader.get_pages_generator()
        self.page_1 = next(pages_generator)
        self.text_reader = TextReader(self.page_1)
        self.info = PDFObjectInfo(self.page_1)

    def test_info(self):
        text = {'译讯科技\n': [90.0, 78.25400000000002]}
        box = self.text_reader.get_all_text_box()[0]
        result = self.info.get_text_box_info(box)
        self.assertEqual(text, result)

    def test_chars_info(self):
        text = [['译', 20.519999999999982, 'HYUHQC+DroidSansFallback', 90.0, 78.25400000000002]]
        char = self.text_reader.get_all_text_char()[0]
        result = self.info.get_char_info(char)
        self.assertEqual(text, result)

    def test_convert_LTChar2EsonChar(self):
        char = self.text_reader.get_all_text_char()[0]
        result = self.text_reader.convert_LTChar2EsonChar(char)
        self.assertEqual(result.set_coordination_in_page(1), 1)

    def tearDown(self) -> None:
        self.data.close()
