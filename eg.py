from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# URL of the webpage
url = "http://example.com/"

# Path to ChromeDriver (Windows version)
chromedriver_path = "/mnt/c/Users/maxlo/OneDrive/Pictures/Screenshots/chat/chromedriver-win64/chromedriver.exe"

# Path to Chrome executable on Windows
chrome_path = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"

# Set up Chrome options
chrome_options = Options()
chrome_options.binary_location = chrome_path

# Initialize the WebDriver service
service = Service(chromedriver_path)

# Start the WebDriver and Chrome
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the webpage
    driver.get(url)

    # Wait for the page to load
    time.sleep(3)  # Wait for 3 seconds

    # Extract the title of the webpage
    title = driver.find_element(By.TAG_NAME, "h1").text
    print("Title:", title)

    # Extract the paragraph text
    paragraph = driver.find_element(By.TAG_NAME, "p").text
    print("Paragraph:", paragraph)

finally:
    # Close the WebDriver
    driver.quit()
