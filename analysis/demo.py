import fitz

#  官方文档地址: https://pymupdf.readthedocs.io/


class GeneratorImg:
    def __init__(self, img_data):
        self.img_data = img_data

    def read_file(self):
        doc = fitz.open(self.img_data)
        return doc

    def get_file_page(self):
        for page in self.read_file():
            text = page.get_text('dict')
            img_info = text['blocks']
            return img_info

    def get_img_info(self):
        for img_info in self.get_file_page():
            if 'ext' in img_info.keys():
                return img_info

