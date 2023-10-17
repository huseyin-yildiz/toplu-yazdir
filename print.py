from pdf_split import split_pdf
import win32api
import win32print

GHOSTSCRIPT_PATH = ".\\GHOSTSCRIPT\\bin\\gswin32.exe"
GSPRINT_PATH = ".\\GSPRINT\\gsprint.exe"

def print_pdf(pdf_path):
    currentprinter = win32print.GetDefaultPrinter()
    win32api.ShellExecute(0, 'open', GSPRINT_PATH, '-ghostscript "'+GHOSTSCRIPT_PATH+'" -printer "'+currentprinter+'" "' + pdf_path +'" ', '.', 0)


if __name__ == "__main__":
    input_pdf = "test2.pdf"

    output_pdf1 = "output_pdf1.pdf"
    output_pdf2 = "output_pdf2.pdf"
    
    split_pdf(input_pdf, output_pdf1, output_pdf2)
    print_pdf(output_pdf1)
    input("Yazdirma tamamlaninca sayfalarin yonunu degistirmeden yerlestir ve enter bas")
    print_pdf(output_pdf2)
    print("Yazdırma tamamlandı")

