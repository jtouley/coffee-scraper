import requests
from bs4 import BeautifulSoup
import datetime

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data with status code {response.status_code}")

def parse_html(html):
    return BeautifulSoup(html, 'html.parser')

def extract_data(soup):
    # Target the <ul> element that contains all the coffee items
    coffee_list_container = soup.find('ul', class_='grid grid-cols-2 xl:grid-cols-3')
    # Assuming each coffee item is an <li> element within this <ul>
    coffee_list = coffee_list_container.find_all('li')
    data = []
    for coffee in coffee_list:
        origin = coffee.find('p', class_='mb-3 lg:mb-4 uppercase text-xs md:text-sm lg:text-base tracking-wider font-freight-sans')
        name = coffee.find('h3', class_='text-2xl md:text-3xl xl:text-4xl md:mb-2 lg:mb-3 mb-2 font-acorn-semibold')
        tasting_notes = coffee.find('p', class_='italic font-freight-sans font-medium text-xs md:text-base xl:text-lg')
        price = coffee.find('p', class_='text-lg xl:text-2xl font-acorn-semibold js-price')
        roast_type = coffee.find('p', class_='uppercase text-sm tracking-wider font-freight-sans')

        # Check if all elements are found before adding to the data list
        if all([origin, name, price, roast_type, tasting_notes]):
            data.append({
                "name": name.text.strip(),
                "price": price.text.strip(),
                "roast_type": roast_type.text.strip(),
                "tasting_notes": tasting_notes.text.strip(),
                "origin": origin.text.strip()
            })
    return data

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write("Name,Price,Roast Type,Tasting Notes,Origin\n")
        for item in data:
            file.write(f'{item["name"]},{item["price"]},{item["roast_type"]},{item["tasting_notes"]},{item["origin"]}\n')

def scrape_coffee_data(url):
    html = fetch_page(url)
    soup = parse_html(html)
    data = extract_data(soup)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    roaster = url.split('/')[-3].split('.')[0]
    filename = f"data/{roaster}_{today}.txt"
    save_to_file(data, filename)
    print(f"Data saved to {filename}")

# Example usage
scrape_coffee_data('https://counterculturecoffee.com/collections/coffee')
