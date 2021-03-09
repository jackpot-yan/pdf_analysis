from analysis.text_detection import PDFReader
from unittest import TestCase
import os


class Tester(TestCase):
    def setUp(self) -> None:
        absolute_path = os.path.dirname(__file__)
        file_path = os.path.join(absolute_path, 'test_files/pages.pdf')
        self.data = open(file_path, 'rb')

    def test_read_page_count(self):
        pdf_reader = PDFReader(self.data)
        page_count = pdf_reader.get_page_count()
        self.assertEqual(1, page_count)

    def tearDown(self) -> None:
        self.data.close()
