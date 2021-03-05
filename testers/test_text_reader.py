from unittest import TestCase
from analysis.text_detection import PDFReader, TextReader, LTTextBox, LTTextLine
from testers import test_pdf


class Tester(TestCase):
    def setUp(self) -> None:
        self.data = open(test_pdf, 'rb')
        pdf_reader = PDFReader(self.data)
        pages_generator = pdf_reader.get_pages_generator()
        self.page_1 = next(pages_generator)
        self.text_reader = TextReader(self.page_1)

    def test_get_page_size(self):
        result = self.text_reader.get_page_size()
        self.assertEqual({'width': 595.3, 'height': 841.9}, result)

    def test_text_box(self):
        result = self.text_reader.get_all_text_box()
        self.assertEqual(3, len(result))
        self.assertIsInstance(result[0], LTTextBox)
        self.assertIn('译讯科技', str(result[0]))
        self.assertIn('研发部', str(result[1]))
        self.assertIn('袁晓彤', str(result[2]))
        result_ = self.text_reader.get_text_line_from_text_box(result[0])
        self.assertEqual(1, len(result_))
        self.assertIsInstance(result_[0], LTTextLine)
        result_2 = self.text_reader.get_text_char_from_text_line(result_[0])
        self.assertEqual(4, len(result_2))

    def test_text_line(self):
        result = self.text_reader.get_all_text_line()
        self.assertEqual(3, len(result))

    def test_all_get_char(self):
        result = self.text_reader.get_all_text_char()
        self.assertIn('译', str(result[0]))

    def tearDown(self) -> None:
        self.data.close()
