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
        text = ('译讯科技\n', [90.0, 78.25400000000002, 4])
        result = list(self.info.get_all_text_box_info().items())[0]
        self.assertEqual(text, result)

    def test_chars_info(self):
        text = ['译', 20.519999999999982, 'HYUHQC+DroidSansFallback', 90.0, 78.25400000000002]
        result = self.info.get_all_char_info()[0]
        self.assertEqual(text, result)

    def tearDown(self) -> None:
        self.data.close()
