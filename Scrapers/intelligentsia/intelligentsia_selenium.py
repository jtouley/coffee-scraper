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

try:
    driver.get('https://www.intelligentsia.com/collections/coffee#?page=1/filter.tags_coffee_type=Single%20Origin/sort.ss_price=asc')
    
    # Use WebDriverWait to wait for a specific element to be loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.pi__desc'))
    )
    
    # Now you can parse the page using driver.page_source
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Collecting all data into a structured way
    products = soup.find_all('div', class_='pi__desc')  # Using the div class you specified
    
    # Lists to store product data
    titles = []
    prices = []
    flavors = []
    
    for product in products:
        title = product.find('h3', class_='pi__title').text.strip() if product.find('h3', class_='pi__title') else 'No Title Found'
        price = product.find('p', class_='pi__price').text.strip() if product.find('p', class_='pi__price') else 'No Price Found'
        flavor_element = product.find('ul', class_='pi__flavors')
        flavor = flavor_element.find('li', class_='pi__flavor').text.strip() if flavor_element and flavor_element.find('li', class_='pi__flavor') else 'Null'  # Default to 'Null' if not found
        
        titles.append(title)
        prices.append(price)
        flavors.append(flavor)

    # Creating a DataFrame
    df = pd.DataFrame({
        'Title': titles,
        'Price': prices,
        'Flavors': flavors
    })
    
    # Create 'data' directory if it doesn't exist
    data_directory = 'data'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    
    # Generating a datetime string for the filename
    datetime_string = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'data/intelligentsia_{datetime_string}.csv'
    
    # Saving to CSV
    df.to_csv(filename, index=False)
    print(f'Data saved to {filename}')

finally:
    # Clean up: close the browser window
    driver.quit()
