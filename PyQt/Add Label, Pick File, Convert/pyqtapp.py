import sys
import os
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.colors import white
from io import BytesIO
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel

class PDFLabelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Widgets for Label 1
        self.labelInput1 = QLineEdit(self)
        self.labelInput1.setPlaceholderText("Enter your first label here")

        # Widgets for Label 2
        self.labelInput2 = QLineEdit(self)
        self.labelInput2.setPlaceholderText("Enter your second label here")

        self.pathButton = QPushButton("Select Folder", self)
        self.pathButton.clicked.connect(self.showDialog)
        self.folderLabel = QLabel("", self)
        

        self.convertButton = QPushButton("Convert PDFs", self)
        self.convertButton.clicked.connect(self.convertPDFs)

        self.statusLabel = QLabel("", self)

        # Add widgets to layout
        layout.addWidget(self.labelInput1)
        layout.addWidget(self.labelInput2)
        layout.addWidget(self.pathButton)
        layout.addWidget(self.folderLabel)
        layout.addWidget(self.convertButton)
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)
        self.setWindowTitle("PDF Label App")
        self.setGeometry(300, 300, 300, 200)
        
        

    def showDialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.selectedFolderPath = folder_path
            self.folderLabel.setText(self.selectedFolderPath)

    def convertPDFs(self):
        label1 = self.labelInput1.text()
        label2 = self.labelInput2.text()
        if hasattr(self, 'selectedFolderPath') and (label1 or label2):
            self.main(self.selectedFolderPath, label1, label2)
            self.statusLabel.setText("Conversion Complete!")
        else:
            self.statusLabel.setText("Please provide folder and at least one label!")

    def add_label_to_pdf_page(self, page, label1, label2, page_width, page_height):
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        font_size = 50  # Adjust font size as necessary
        
        # Split the label into two lines
        label_line1 = label1
        label_line2 = label2
        
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

    def add_label_to_pdf(self, pdf_path, label1, label2):
        output = PdfWriter()
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                page = self.add_label_to_pdf_page(page, label1, label2, page.mediabox[2], page.mediabox[3])
                output.add_page(page)
            with open(pdf_path, "wb") as output_file:
                output.write(output_file)

    def main(self, folder_path, label1, label2):
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith('.pdf'):
                pdf_path = os.path.join(folder_path, file_name)
                self.add_label_to_pdf(pdf_path, label1, label2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFLabelApp()
    ex.show()
    sys.exit(app.exec_())
