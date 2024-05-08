import requests
from bs4 import BeautifulSoup
import datetime

def scrape_coffee_data(url):
    # Parse the base URL to get the roaster name
    roaster = url.split('/')[-2]  # Adjust based on URL structure

    # Send a GET request to the website
    response = requests.get(url)
    
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find elements containing coffee data
    coffee_list = soup.find_all('div', class_='grid__item')  # Adjust if necessary
    
    # Prepare to write to file
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"data/{roaster}_{today}.txt"
    with open(filename, 'w') as file:
        file.write("Name,Price,Roast Type,Tasting Notes,Origin\n")
        
        # Extract data from each coffee item
        for coffee in coffee_list:
            name = coffee.find('h3', class_='font-acorn-semibold')
            price = coffee.find('p', class_=lambda x: 'js-price' in x.split() and 'line-through' not in x.split())
            roast_type = coffee.find('p', class_='uppercase', text=lambda text: 'roast' in text.lower())
            tasting_notes = coffee.find('p', class_='italic')
            origin = coffee.find('p', class_='uppercase', text=lambda text: 'single-origin' in text.lower())

            if name and price and roast_type and tasting_notes and origin:
                file.write(f"{name.text.strip()},{price.text.strip()},{roast_type.text.strip()},{tasting_notes.text.strip()},{origin.text.strip()}\n")
                
    print(f"Data saved to {filename}")

# Example usage
scrape_coffee_data('https://counterculturecoffee.com/collections/all')
