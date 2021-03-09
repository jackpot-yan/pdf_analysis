import fitz

#  官方文档地址: https://pymupdf.readthedocs.io/


def demo(file_path):
    """
    # ...
    :param file_path: 待解析的文件路径
    :return: None
    """
    doc = fitz.open(file_path)
    for page in doc:
        text = page.get_text('html').encode('utf8')
        with open('text.html', 'wb') as file:
            file.write(text)


demo('../testers/test_files/test.pdf')
