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
    coffee_list_container = soup.find('ul', class_='grid md:grid-cols-3 gap-y-md md:gap-y-10 gap-[6px] md:gap-x-4 lg:gap-x-5  grid-cols-2')
    # Assuming each coffee item is an <li> element within this <ul>
    coffee_list = coffee_list_container.find_all('li')
    data = []
    for coffee in coffee_list:
        name = coffee.find('p', class_='font-serif text-black text-md h-14 md:h-10 md:text-xl')
        tasting_notes = coffee.find('p', class_='font-serif text-grey text-xs mb-4 md:mb-2 sm:text-md')
        price = coffee.find('span', attrs={'data-test-id': 'price-regular'})
        roast_type = coffee.find('p', class_='font-sans tracking-widest uppercase text-black text-xs xl:text-sm mt-auto font-normal')

        # Check if all elements are found before adding to the data list
        if all([name, price, roast_type, tasting_notes]):
            data.append({
                "name": name.text.strip() if name else 'Unknown',
                "price": price.text.strip() if price else 'Unknown',
                "roast_type": roast_type.text.strip() if roast_type else 'Unknown',
                "tasting_notes": tasting_notes.text.strip() if tasting_notes else 'Unknown'
            })
    return data

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write("Name,Price,Roast Type,Tasting Notes\n")
        for item in data:
            file.write(f'{item["name"]},{item["price"]},{item["roast_type"]},{item["tasting_notes"]}\n')

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
scrape_coffee_data('https://bluebottlecoffee.com/us/eng/collection/single-origin')
