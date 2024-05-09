from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the chromedriver
chromedriver_path = '/opt/homebrew/Caskroom/chromedriver/124.0.6367.155/chromedriver-mac-arm64/chromedriver'  # Replace with your actual path

service = Service(executable_path=chromedriver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.intelligentsia.com/collections/coffee#?page=1/filter.tags_coffee_type=Single%20Origin/sort.ss_days_since_published=asc')

# Wait for the page to load and check for the popup
try:
    # Wait for the close button of the popup to be clickable
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.css-oohciz")))
    close_button = driver.find_element(By.CSS_SELECTOR, "svg.css-oohciz")
    close_button.click()
    print("Popup closed successfully.")
except Exception as e:
    print("No popup found or error closing popup:", str(e))

# Proceed with data extraction
try:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3.font-acorn-semibold')))
    coffee_names = driver.find_elements(By.CSS_SELECTOR, 'h3.font-acorn-semibold')
    prices = driver.find_elements(By.CSS_SELECTOR, 'p.js-price')
    roast_types = driver.find_elements(By.CSS_SELECTOR, 'p.font-freight-sans.uppercase')
    tasting_notes = driver.find_elements(By.CSS_SELECTOR, 'p.font-freight-sans.italic')
    origins = driver.find_elements(By.CSS_SELECTOR, 'p.font-freight-sans.mb-3')

    for name, price, roast_type, note, origin in zip(coffee_names, prices, roast_types, tasting_notes, origins):
        print("Name:", name.text if name.text else "N/A")
        print("Price:", price.text if price.text else "N/A")
        print("Roast Type:", roast_type.text if roast_type.text else "N/A")
        print("Tasting Notes:", note.text if note.text else "N/A")
        print("Origin:", origin.text if origin.text else "N/A")
        print("------")

finally:
    driver.quit()