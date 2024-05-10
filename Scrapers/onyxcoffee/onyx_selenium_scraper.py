import os
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Path to the chromedriver
chromedriver_path = '/opt/homebrew/Caskroom/chromedriver/124.0.6367.155/chromedriver-mac-arm64/chromedriver'
service = Service(executable_path=chromedriver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Define the main page URL and base product URL
main_page_url = "https://onyxcoffeelab.com/collections/coffee/"
base_product_url = "https://onyxcoffeelab.com/products/"

# Load the main page
driver.get(main_page_url)

# Wait for the page to load completely (you might need to adjust the wait time)
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-preview")))

# Scroll down to ensure all content is loaded
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Get the page source after scrolling
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Find all product names
product_names = [name.text.strip() for name in soup.select("h3.title.upper")]

# Generate product URLs
product_urls = [base_product_url + name.replace(" ", "-") for name in product_names]

# Print product names and URLs
print("\nProduct Names and URLs:")
for product_name, product_url in zip(product_names, product_urls):
    print(f"Product Name: {product_name}, URL: {product_url}")

# Exclude the "Doyenne" product URL
excluded_product_urls = [
    "https://onyxcoffeelab.com/products/Doyenne",
    "https://onyxcoffeelab.com/products/The-Duet"
]

# Exclude the specified product URLs
for excluded_url in excluded_product_urls:
    if excluded_url in product_urls:
        product_urls.remove(excluded_url)

# Scraping additional details from each product page
for product_url in product_urls:
    driver.get(product_url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".left .top")))

    # Parse the product page source with BeautifulSoup
    product_page_source = driver.page_source
    product_soup = BeautifulSoup(product_page_source, "html.parser")

    # Extract additional details
    product_details = {}
    product_details["Name"] = product_soup.find("h1").text.strip()
    product_details["Description"] = product_soup.select_one(".main-blurb p").text.strip()
    product_details["Price"] = product_soup.select_one(".price.variant-price").text.strip()

    # New selectors for additional details
    product_details["Roast Profile Level"] = product_soup.select_one(".roast-l strong").text.strip() if product_soup.select_one(".roast-l strong") else "N/A"
    product_details["Cup"] = product_soup.select_one(".m-coffee-stats .a-feature:nth-child(4) .value").text.strip() if product_soup.select_one(".m-coffee-stats .a-feature:nth-child(4) .value") else "N/A"
    product_details["Origin"] = product_soup.select_one(".m-coffee-stats .a-feature:nth-child(1) .value").text.strip() if product_soup.select_one(".m-coffee-stats .a-feature:nth-child(1) .value") else "N/A"
    product_details["Process"] = product_soup.select_one(".m-coffee-stats .a-feature:nth-child(2) .value").text.strip() if product_soup.select_one(".m-coffee-stats .a-feature:nth-child(2) .value") else "N/A"
    product_details["Elevation"] = product_soup.select_one(".m-coffee-stats .a-feature:nth-child(3) .value").text.strip() if product_soup.select_one(".m-coffee-stats .a-feature:nth-child(3) .value") else "N/A"

    # Print the product details
    print("\nProduct Details:")
    for key, value in product_details.items():
        print(f"{key}: {value}")

# Close the WebDriver
driver.quit()
