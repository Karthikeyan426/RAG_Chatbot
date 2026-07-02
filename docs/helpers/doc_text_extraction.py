import fitz

def extractText(file):
    print('extract text')
    file.seek(0)  

    pdf_bytes = file.read()

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    for page in doc:
        page_text = page.get_text()
        if page_text:
            text += page_text

    doc.close()

    return text