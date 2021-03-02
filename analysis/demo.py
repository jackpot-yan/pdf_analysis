import fitz
import pprint


def pdfimg(file_path):
    """
    # 实验文件
    :param file_path: 示例文件
    :return: None
    """
    doc = fitz.open(file_path)
    for i in range(537):
        print(doc.extract_image(i))
    for page in range(doc.pageCount):
        page = doc[page]
        pm = page.getPixmap()
        page_data = pm.getImageData()
        # print(page_data)


def demo(file_path):
    with open(file_path, 'rb') as f:
        pprint.pprint(str(f.read()))


demo('../002-英译中PDF+.pdf')
