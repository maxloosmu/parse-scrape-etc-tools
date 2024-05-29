import pytesseract
from PIL import Image
import pandas as pd
import os

# Define the folder containing the images
folder_path = "."

# Initialize an empty list to store the data
all_data = []

# Process each PNG file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        image_path = os.path.join(folder_path, filename)
        print(f"Processing {image_path}")
        
        # Load the image using PIL
        image = Image.open(image_path)
        
        # Perform OCR on the image
        ocr_data = pytesseract.image_to_string(image)
        
        # Split the OCR data into lines
        lines = ocr_data.split('\n')
        
        # Process the lines to create structured data
        for line in lines:
            if line.strip():  # Check if the line is not empty
                columns = line.split()
                all_data.append(columns)

# Convert the combined data into a DataFrame
df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
output_csv_path = "extracted_data_combined.csv"
df.to_csv(output_csv_path, index=False)

print(f"Data extracted and saved to {output_csv_path}")
