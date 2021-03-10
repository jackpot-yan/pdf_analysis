from analysis.text_detection import *


class Generator:
    def __init__(self, page):
        self.page = page
        self.text_reader = TextReader(self.page)
        self.info = PDFObjectInfo(self.page)

    def generator_div_label(self):
        page_set = self.text_reader.get_page_size()
        text = '<div id="page0" style="position:relative;width:{0}pt;height:{1}pt;background-color:white">'.format(page_set['width'], page_set['height'])
        return text

    def generator_div_and_p_label(self, lt_box):
        paragraph_set = list(self.info.get_text_box_info(lt_box).values())[0]
        text = """<p style="position:absolute;white-space:pre;margin:0;padding:0;top:{0}pt;left:{1}pt">""".format(paragraph_set[1], paragraph_set[0])
        content = self.generator_div_label() + '\n\t' + text
        return content

    def generator_text_html(self, lt_char):
        font_set = self.info.get_char_info(lt_char)[0]
        text = """<span style="font-family:DroidSansFallback,serif;font-size:{0}pt">{1}</span>""".format(font_set[1], font_set[0])
        return self.generator_div_and_p_label(lt_char) + text
