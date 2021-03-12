import fitz


#  官方文档地址: https://pymupdf.readthedocs.io/


class GeneratorImg:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        doc = fitz.open(self.file_path)
        return doc

    def get_pages_info(self):
        page_info = []
        for page in self.read_file():
            text = page.get_text('dict')
            if text['blocks']:
                page_info.append(text['blocks'])
        return page_info

    def get_image_from_page(self):
        image_info = []
        for page in self.get_pages_info():
            for i in page:
                if 'ext' in i.keys():
                    image_info.append(i)
        return image_info


class EsonImgInfo(GeneratorImg):
    def Eson_image_width(self):
        for i in self.get_image_from_page():
            print(i)
