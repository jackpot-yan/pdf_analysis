from unittest import TestCase
from generator_file import *
import os


class Tester(TestCase):
    def setUp(self) -> None:
        absolute_path = os.path.dirname(__file__)
        file_path = os.path.join(absolute_path, 'test_files/test_img.pdf')
        self.data = fitz.open(file_path)
        self.img_info = GeneratorImg(self.data)

    def test_img_generator(self):
        text_length = (119.05500030517578, 153.04376220703125, 408.1609802246094, 315.78076171875)
        result = self.img_info.get_image_from_page()[0]['bbox']
        self.assertEqual(text_length, result)

    def test_change_info(self):
        width = 270
        height = 152

    def tearDown(self) -> None:
        self.data.close()
