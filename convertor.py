import os
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.lib.colors import white, black

def add_label_to_pdf_page(page, label, page_width, page_height):
    # Create a memory buffer to hold the PDF data
    packet = BytesIO()
    
    # Create a new canvas with the size of the current PDF page
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))
    
    # Define font size for the label
    font_size = 50
    
    # Define the two lines of the label
    label_line1 = "Saifee Light House"
    label_line2 = "+918888076752"
    
    # Calculate the width of each line of the label
    text_width1 = c.stringWidth(label_line1, "Helvetica", font_size)
    text_width2 = c.stringWidth(label_line2, "Helvetica", font_size)
    
    # Calculate x-coordinates for center alignment of each line of the label
    x1 = (page_width - text_width1) / 2
    x2 = (page_width - text_width2) / 2
    
    # Calculate y-coordinates for vertical placement of the label
    y_middle1 = (page_height / 2) + (font_size / 2) + 20  # First line
    y_middle2 = (page_height / 2) - (font_size / 2) - 20  # Second line
    
    # Set font and color for the label
    c.setFont("Helvetica", font_size)
    c.setFillColor(white)
    
    # Draw the label lines on the canvas
    c.drawString(x1, y_middle1, label_line1)
    c.drawString(x2, y_middle2, label_line2)

    # Save the canvas to the memory buffer
    c.save()

    # Reset the memory buffer position to the start
    packet.seek(0)
    
    # Create a new PDF from the canvas in the memory buffer
    new_pdf = PdfReader(packet)
    
    # Overlay the new PDF onto the original page
    page.merge_page(new_pdf.pages[0])
    
    return page

def add_label_to_pdf(pdf_path, label):
    # Create a new empty PDF to store the labeled pages
    output = PdfWriter()
    
    # Open the source PDF for reading
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        # Process each page in the source PDF
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            # Add label to the current page
            page = add_label_to_pdf_page(page, label, page.mediabox[2], page.mediabox[3])
            # Add the labeled page to the output PDF
            output.add_page(page)
        
        # Write the output PDF back to the same file
        with open(pdf_path, "wb") as output_file:
            output.write(output_file)

def main(folder_path, label):
    # Process each file in the provided folder
    for file_name in os.listdir(folder_path):
        # Check if the file is a PDF
        if file_name.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            # Add label to the current PDF
            add_label_to_pdf(pdf_path, label)

# Specify the source folder and label
folder_path = r'C:\Users\Mustafa\Desktop\SLH\LightVendor\ConvertAllAtOnce'
label = 'Saifee Light House - +918888076752'

# Start the labeling process
main(folder_path, label)
