import PyPDF2

def split_pdf(input_pdf, output_pdf1, output_pdf2):
    pdf1 = PyPDF2.PdfWriter()
    pdf2 = PyPDF2.PdfWriter()
    
    with open(input_pdf, "rb") as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        

        for page_num in range(len(pdf_reader.pages)):
            if page_num % 2 == 0:
                pdf1.add_page(pdf_reader.pages[page_num])
            else:
                pdf2.add_page(pdf_reader.pages[page_num])
    
        if(len(pdf_reader.pages) % 2 == 1):
                pdf2.add_blank_page()

    

    with open(output_pdf1, "wb") as output_file1:
        pdf1.write(output_file1)
    
    with open(output_pdf2, "wb") as output_file2:
        pdf2_reversed = PyPDF2.PdfWriter()
        for page in reversed(pdf2.pages):
            rotated_page = page.rotate(180)
            pdf2_reversed.add_page(rotated_page)
        pdf2_reversed.write(output_file2)


def merge_pdfs(pdfs, merged_name):

    merger = PyPDF2.PdfWriter()

    for pdf in pdfs:
        merger.append(pdf)
        if (len(merger.pages) % 2 == 1):
            merger.add_blank_page()

    merger.write(merged_name)
    merger.close()
    return len(merger.pages)



if __name__ == "__main__":
    input_pdf = "test2.pdf"
    output_pdf1 = "output_pdf1.pdf"
    output_pdf2 = "output_pdf2.pdf"
    
    split_pdf(input_pdf, output_pdf1, output_pdf2)


