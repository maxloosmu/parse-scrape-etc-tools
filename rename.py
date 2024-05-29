import PyPDF2
import os

def set_pdf_title_to_filename(pdf_path):
    # Extract the base name without extension as the title
    title = os.path.splitext(os.path.basename(pdf_path))[0]

    # Open the original PDF
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Copy all pages to the writer
        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        # Set the document title
        writer.add_metadata({
            '/Title': title
        })

        # Write the changes back to the original PDF file
        with open(pdf_path, 'wb') as output_file:
            writer.write(output_file)

    print(f'Title set to "{title}" for PDF: {pdf_path}')

def process_all_pdfs_in_folder():
    # Get the current directory
    folder_path = os.path.dirname(os.path.abspath(__file__))

    # Iterate through all files in the directory
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            set_pdf_title_to_filename(pdf_path)

# Run the script
process_all_pdfs_in_folder()
