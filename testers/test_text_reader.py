from unittest import TestCase
from analysis.text_detection import PDFReader, TextReader
import os


class Tester(TestCase):
    def setUp(self) -> None:
        absolute_path = os.path.dirname(__file__)
        file_path = os.path.join(absolute_path, 'test_files/test.pdf')
        self.data = open(file_path, 'rb')
        pdf_reader = PDFReader(self.data)
        pages_generator = pdf_reader.get_pages_generator()
        self.page_1 = next(pages_generator)

    def test_text_box(self):
        text_reader = TextReader(self.page_1)
        result = text_reader.get_all_text_box()
        self.assertEqual(3, len(result))
        self.assertIn('译讯科技', str(result[0]))
        self.assertIn('研发部', str(result[1]))
        self.assertIn('袁晓彤', str(result[2]))

    def test_text_line(self):
        text_reader = TextReader(self.page_1)
        result = text_reader.get_all_text_line()
        self.assertEqual(3, len(result))

    def tearDown(self) -> None:
        self.data.close()
