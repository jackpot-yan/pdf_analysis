from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LTTextBox, LTTextLine, LTChar, LTFigure
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument

path = '/home/jackpot/PycharmProjects/pdf_analysis/002-英译中PDF+.pdf'


def page_number(file_path):
    text = []
    with open(file_path, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize()
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if isinstance(x, LTFigure) or isinstance(x, LTTextBox):
                    for o in x:
                        if isinstance(o, LTChar):
                            text.append(o.get_text())
    return ''.join(text)


print(page_number(path))
