import os
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.lib.colors import white, black

def add_label_to_pdf_page(page, label, page_width, page_height):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))
    
    font_size = 50  # Adjust font size as necessary
    
    # Split the label into two lines
    label_line1 = "Saifee Light House"
    label_line2 = "+918888076752"
    
    text_width1 = c.stringWidth(label_line1, "Helvetica", font_size)
    text_width2 = c.stringWidth(label_line2, "Helvetica", font_size)
    
    # Center alignment for both lines
    x1 = (page_width - text_width1) / 2
    x2 = (page_width - text_width2) / 2
    
    # Vertical alignment for two lines
    # Using a little offset (like 20) to give some space between the lines
    y_middle1 = (page_height / 2) + (font_size / 2) + 20  
    y_middle2 = (page_height / 2) - (font_size / 2) - 20  
    
    c.setFont("Helvetica", font_size)
    c.setFillColor(white)  # <-- Setting fill color to white
    c.drawString(x1, y_middle1, label_line1)
    c.drawString(x2, y_middle2, label_line2)

    c.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)
    page.merge_page(new_pdf.pages[0])
    return page


def add_label_to_pdf(pdf_path, label):
    output = PdfWriter()
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            page = add_label_to_pdf_page(page, label, page.mediabox[2], page.mediabox[3])
            output.add_page(page)
        with open(pdf_path, "wb") as output_file:
            output.write(output_file)

def main(folder_path, label):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            add_label_to_pdf(pdf_path, label)

# Provide the folder path and label here
folder_path = r'C:\Users\Mustafa\Desktop\SLH\Vinit\ConvertAllAtOnce'  # Change this to your folder path
label = 'Saifee Light House - +918888076752'
main(folder_path, label)