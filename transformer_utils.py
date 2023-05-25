import PyPDF2
import pdfplumber
import pandas as pd


def parse_pdf(pdf_path):
    text_pages = []
    images = []
    tables = []

    # 解析文本页
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for i in range(num_pages):
            page = reader.pages[i]
            text = page.extract_text()
            text_pages.append(text)

    

    # 解析图片和表格
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 解析图片
            extracted_images = page.images
            images.extend(extracted_images)

            # 解析表格
            extracted_tables = page.extract_tables()
            for table in extracted_tables:
                df = pd.DataFrame(table[1:], columns=table[0])
                tables.append(df)

    return text_pages, images, tables