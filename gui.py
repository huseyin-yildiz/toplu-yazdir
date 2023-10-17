import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox
import os
import print
import win32print
import pdf_split
import sys


FRONT_COVER_PATH = "front.pdf"
BACK_COVER_PATH = "back.pdf"
MERGED_PATH = "merged.pdf"
PAGE_PRINT_SIZE_PER_MIN = 12

def add_new_files():
    file_paths = filedialog.askopenfilenames(title="Select files to print", filetypes=[("PDF files", "*.pdf")])
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        copy_size_table.insert('', 'end', values=(file_name, 1, file_path))  # Default copy size is 1


def remove_selected_files():
    selected_items = copy_size_table.selection()
    for item in selected_items:
        copy_size_table.delete(item)

def print_files():
    printer_name = printer_var.get()
    file_paths = []
    for item in copy_size_table.get_children():
        file_name, copy_size, file_path = copy_size_table.item(item, 'values')
       # print("Printing", file_name, "with", copy_size, "copies on", printer_name)
        #print("Printing:", file_name)
        for _ in range(int(copy_size)): 
            file_paths.append(file_path)
    merged_page_size = pdf_split.merge_pdfs(file_paths, MERGED_PATH)
    os.system( "attrib +h "+MERGED_PATH )       # hide the file

    pdf_split.split_pdf(MERGED_PATH, FRONT_COVER_PATH, BACK_COVER_PATH)
    os.system( "attrib +h "+FRONT_COVER_PATH )       # hide the file
    os.system( "attrib +h "+BACK_COVER_PATH )       # hide the file
    

    print.print_pdf(FRONT_COVER_PATH)
    elapse_time = round( (merged_page_size / 2 )  / PAGE_PRINT_SIZE_PER_MIN )
    elapse_time = 1 if elapse_time < 1 else elapse_time
    
    tk.messagebox.showinfo(message=f"Tahmini Süre:{elapse_time} dk. Yazdirma tamamlaninca sayfalarin yonunu degistirmeden yerlestir ve tamam'a bas.")
    print.print_pdf(BACK_COVER_PATH)
    


def increase_copy_size():
    selected_items = copy_size_table.selection()
    for item in selected_items:
        values = copy_size_table.item(item, 'values')
        new_values = (values[0], int(values[1]) + 1, values[2])
        copy_size_table.item(item, values=new_values)

def decrease_copy_size():
    selected_items = copy_size_table.selection()
    for item in selected_items:
        values = copy_size_table.item(item, 'values')
        current_copy_size = int(values[1])
        if current_copy_size > 1:
            new_values = (values[0], current_copy_size - 1, values[2])
            copy_size_table.item(item, values=new_values)

root = tk.Tk()
root.title("Toplu-Yazdır")

# Create a Treeview widget for the table
copy_size_table = ttk.Treeview(root, columns=("File Name", "Copy Size"), show="headings")
copy_size_table.heading("File Name", text="Dosya Adı", anchor='w')
copy_size_table.heading("Copy Size", text="Kopya Sayısı")
copy_size_table.column("Copy Size", width=80)  # Adjust the width as needed
copy_size_table.grid(row=2, column=0, rowspan=5, columnspan=5, padx=10, pady=10)

# New Files button
tk.Button(root, text="Dosya Ekle", command=add_new_files).grid(row=2, column=5, padx=10, pady=10)

# Remove Selected Files button
tk.Button(root, text="Seçili olanları Çıkar", command=remove_selected_files).grid(row=2, column=6, padx=10, pady=10)

# Plus button
tk.Button(root, text="+", command=increase_copy_size).grid(row=3, column=5, padx=10, pady=10)

# Minus button
tk.Button(root, text="-", command=decrease_copy_size).grid(row=3, column=6, padx=10, pady=10)

# Printer selection
tk.Label(root, text="Yazıcı:").grid(row=0, column=0, padx=10, pady=10)
available_printers = win32print.EnumPrinters(2)
default_printer = win32print.GetDefaultPrinter()
printer_var = tk.StringVar()
printer_var.set(default_printer)  # Set the default printer
printer_names = [printer[2] for printer in available_printers]  # Extract printer names
printer_menu = ttk.Combobox(root, textvariable=printer_var, values=printer_names, state="readonly",width=50)
printer_menu.grid(row=0, column=1, columnspan=5,  padx=10, pady=10)
printer_menu.set(default_printer)  # Set the default printer initially

# Print button
tk.Button(root, text="Tüm Dosyaları Yazdır", command=print_files).grid(row=4, column=5, columnspan=2, padx=10, pady=10)

