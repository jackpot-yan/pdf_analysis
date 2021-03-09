from analysis.text_detection import *


class Generator:
    def __init__(self, page):
        self.page = page
        self.info = PDFObjectInfo(page)

    @staticmethod
    def generator_html_head():
        html_header = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>这是一个Demo</title>
        </head>
        <body>
        """
        return html_header

    def generator_font_info_to_html(self, lt_chars):
        font_list = []
        info_list = self.info.get_char_info(lt_chars)
        for info in info_list:
            text = """<span font-size:{0}pt">{1}</span>""".format(info[1], info[0])
            font_list.append(text)
        return font_list

    def generator_paragraph_to_html(self, lt_box):
        p_label_list = []
        paragraph_dict = self.info.get_text_box_info(lt_box)
        for paragraph in paragraph_dict.values():
            text = """<p style="position:absolute;white-space:pre;margin:0;padding:0;top:{0}pt;left:{1}pt"></p>""".format(paragraph[1], paragraph[0])
            p_label_list.append(text)
        return p_label_list

    def generator_page_to_html(self):
        text_reader = TextReader(self.page)
        page_info = text_reader.get_page_size()
        text = """<div id="page0" style="position:relative;width:{0}pt;height:{1}pt;background-color:white">""".format(page_info['width'], page_info['height'])
        return text


class Generator_file(Generator):
    def generator_html_content(self):
        print(self.generator_page_to_html())
