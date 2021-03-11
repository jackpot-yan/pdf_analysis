from analysis.text_detection import *
from analysis.demo import *
import base64


class Generator:
    def __init__(self, page):
        self.page = page
        self.text_reader = TextReader(self.page)
        self.info = PDFObjectInfo(self.page)

    @staticmethod
    def html_header():
        text = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>这是一个demo</title>
</head>
<body>"""
        return text

    def generator_div_label(self):
        page_set = self.text_reader.get_page_size()
        text = '<div id="page0" style="position:relative;width:{0}pt;height:{1}pt;background-color:white">'.format(page_set['width'], page_set['height'])
        return text

    def generator_div_and_p_label(self):
        paragraph_sets = list(self.info.get_all_text_box_info().values())
        for paragraph_set in paragraph_sets:
            text = """<p style="position:absolute;white-space:pre;margin:0;padding:0;top:{0}pt;left:{1}pt">""".format(paragraph_set[1], paragraph_set[0])
            content = self.generator_div_label() + '\n\t' + text
            return content

    def get_current_paragraph_length(self):
        paragraph_sets = list(self.info.get_all_text_box_info().values())
        for paragraph_set in paragraph_sets:
            paragraph_length = paragraph_set[2]
            return paragraph_length

    def generator_text_html(self):

        font_sets = self.info.get_all_char_info()
        span_label_list = []
        for font_set in font_sets:
            text = """<span style="font-family:DroidSansFallback,serif;font-size:{0}pt">{1}</span>""".format(font_set[1], font_set[0])
            span_label_list.extend(text)
        print(span_label_list)
        return self.generator_div_and_p_label() + ''.join(span_label_list) + '</p>'

    @staticmethod
    def generator_img_html(img_data):
        img_info = GeneratorImg(img_data)
        img = img_info.get_img_info()
        text = """<img style="position:absolute;top:{0}pt;left:{1}pt;width:{2}px;height:{3}px" src="data:image/{4};base64,{5}">""" \
            .format(img['bbox'][1], img['bbox'][0], img['width'], img['height'], img['ext'], base64.b64encode(img['image']).decode('utf8'))
        return text

    def generator_html_file(self, img_data):
        text = self.html_header() + self.generator_text_html() + '\n\t' + self.generator_img_html(img_data) + '\n' + '</div>'
        with open('demo.html', 'w+') as file:
            file.write(text)


if __name__ == '__main__':
    file_path = './testers/test_files/test_img.pdf'

    with open(file_path, 'rb') as f:
        flag = 0
        func = PDFReader(f)
        pdf_page = next(func.get_pages_generator())
        pdf_info = TextReader(pdf_page)
        data = fitz.open(file_path)
        Generator(pdf_page).generator_html_file(data)
