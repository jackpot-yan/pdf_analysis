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
        text = '<div style="position:relative;width:{0}pt;height:{1}pt;">'.format(page_set['width'], page_set['height'])
        return text

    def generator_p_label(self):
        paragraph_sets = list(self.info.get_all_text_box_info().values())
        for paragraph_set in paragraph_sets:
            text = """<p style="position:absolute; padding:{0}pt {1}pt">""".format(paragraph_set[1], paragraph_set[0])
            yield text, paragraph_set[2]

    def get_current_paragraph_length(self):
        paragraph_sets = list(self.info.get_all_text_box_info().values())
        for paragraph_set in paragraph_sets:
            paragraph_length = paragraph_set[2]
            return paragraph_length

    def generator_all_span_label(self):

        font_sets = self.info.get_all_char_info()
        span_label_list = []
        for font_set in font_sets:
            text = """<span style="font-size: {0}pt; left: {1}pt; top: {2}pt; position: absolute">{3}</span>""".format(font_set[1], font_set[3], font_set[4]
                                                                                                                       , font_set[0])
            span_label_list.append(text)
        return span_label_list

    def splicing_p_and_span(self):
        content = []
        span_label = self.generator_all_span_label()
        for p_label in self.generator_p_label():
            length = p_label[1]
            text = p_label[0] + ''.join(span_label[0:length]) + '</p>'
            del span_label[0:length]
            content.append(text)
        return content

    @staticmethod
    def generator_img_html(img_data):
        img_info = GeneratorImg(img_data)
        images = img_info.get_image_from_page()
        content = []
        for img in images:
            text = """<img style="position:absolute;top:{0}pt;left:{1}pt;width:{2}pt;height:{3}pt" src="data:image/{4};base64,{5}">""" \
                .format(img['bbox'][1], img['bbox'][0], img['width'] / 3, img['height'] / 3, img['ext'], base64.b64encode(img['image']).decode('utf8'))
            content.append(text)
        return content

    def generator_html_file(self, img_data):
        content = self.generator_div_label() + '\n\t' + ''.join(self.splicing_p_and_span()) + '\n\t' + \
                  ''.join(self.generator_img_html(img_data)) + '\n' + '</div>'
        return content


if __name__ == '__main__':
    file_path = './testers/test_files/test_image.pdf'
    text = []

    with open(file_path, 'rb') as f:
        func = PDFReader(f)
        for pdf_page in func.get_pages_generator():
            pdf_info = TextReader(pdf_page)
            data = fitz.open(file_path)
            text.append(Generator(pdf_page).generator_html_file(data))
    with open('text.html', 'w+') as file:
        content = Generator.html_header() + '\n' + ''.join(text)
        file.write(content)
