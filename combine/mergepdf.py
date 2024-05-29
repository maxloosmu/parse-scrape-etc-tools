import PyPDF2
import os

def merge_pdfs(pdf_folder, output_filename):
    # Create a PdfMerger object
    merger = PyPDF2.PdfMerger()

    # Get a list of all PDF files in the specified folder
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    # Sort the PDF files in alphabetical order
    pdf_files.sort()

    # Append each PDF file to the merger
    for pdf in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf)
        merger.append(pdf_path)
        print(f"Added: {pdf}")

    # Write the merged PDF to a file
    output_path = os.path.join(pdf_folder, output_filename)
    merger.write(output_path)
    merger.close()
    print(f'Merged PDF created successfully: {output_path}')

# Folder containing PDF files (same folder as the script)
pdf_folder = os.path.dirname(os.path.abspath(__file__))
# Output PDF file name
output_filename = 'merged_output.pdf'

# Merge the PDF files
merge_pdfs(pdf_folder, output_filename)
