from PIL import Image
from reportlab.pdfgen import canvas
import os

# Function to convert PNG images to PDF
def png_to_pdf(png_files, output_pdf):
    # Create a canvas object
    c = canvas.Canvas(output_pdf)

    for png_file in png_files:
        # Open the image file
        img = Image.open(png_file)
        img_width, img_height = img.size

        # Create a new page with the size of the image
        c.setPageSize((img_width, img_height))
        # Draw the image on the canvas
        c.drawImage(png_file, 0, 0, width=img_width, height=img_height)
        c.showPage()  # Add a new page

    c.save()  # Save the PDF

# Directory containing PNG files
directory = '.'
# List of PNG files in sequential order
png_files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')])

# Output PDF file
output_pdf = 'output.pdf'

# Convert PNG to PDF
png_to_pdf(png_files, output_pdf)

print(f'PDF created successfully: {output_pdf}')
