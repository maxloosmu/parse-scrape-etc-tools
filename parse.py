import pandas as pd
import os

# Get the current directory where the script and paste.txt are located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the file paths relative to the current directory
file_path = os.path.join(current_dir, 'paste.txt')
output_file_path = os.path.join(current_dir, 'stocks_data.csv')

# Read the file content
with open(file_path, 'r') as file:
    lines = file.readlines()

# Strip newlines and remove empty lines
lines = [line.strip() for line in lines if line.strip()]

# Define the column headers
headers = ["Trading Name", "Trading Code", "Last", "Chg", "Chg%", "Vol", "Val($M)", "BVol", "Bid", "Ask", "SVol", "Open", "High", "Low"]

# Initialize the list to hold the rows of the table
data = []

# Parse the lines into rows of data
for i in range(0, len(lines), len(headers)):
    data.append(lines[i:i+len(headers)])

# Create a DataFrame from the parsed data
df = pd.DataFrame(data, columns=headers)

# Write the DataFrame to a CSV file
df.to_csv(output_file_path, index=False)

print(f"Data has been written to {output_file_path}")
