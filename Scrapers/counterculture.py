import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data with status code {response.status_code}")

def parse_html(html):
    return BeautifulSoup(html, 'html.parser')

def extract_data(soup):
    coffee_details = []
    coffee_items = soup.find_all('div', class_='bg-white w-full h-full flex flex-col gap-2 justify-between px-4 xl:px-8 py-4 xl:py-6 animate animate-fadeInUp')
    for coffee in coffee_items:
        origin = coffee.find('p', class_='mb-3 lg:mb-4 uppercase text-xs md:text-sm lg:text-base tracking-wider font-freight-sans').text.strip()
        name = coffee.find('h3', class_='text-2xl md:text-3xl xl:text-4xl md:mb-2 lg:mb-3 mb-2 font-acorn-semibold').text.strip()
        tasting_notes = coffee.find('p', class_='italic font-freight-sans font-medium text-xs md:text-base xl:text-lg').text.strip()
        price = coffee.find('p', class_='text-lg xl:text-2xl font-acorn-semibold js-price').text.strip()
        roast_level = coffee.find('p', class_='uppercase text-sm tracking-wider font-freight-sans').text.strip()

        coffee_details.append({
            "coffee_origin": origin,
            "coffee_name": name,
            "tasting_notes": tasting_notes,
            "price": price,
            "roast_level": roast_level
        })

    return coffee_details


def scrape_coffee_data(url):
    html = fetch_page(url)
    soup = parse_html(html)
    data = extract_data(soup)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    roaster = url.split('/')[-2]
    directory = 'data'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f"{directory}/{roaster}_{today}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for coffee in data:
            file.write(f"Name: {coffee['name']}\n")
            file.write(f"Price: {coffee['price']}\n")
            file.write(f"Roast Level: {coffee['roast_level']}\n")
            file.write(f"Tasting Notes: {coffee['tasting_notes']}\n")
            file.write(f"Origin: {coffee['origin']}\n")
            file.write("------\n")
    return data

# Example usage
url = 'https://counterculturecoffee.com/collections/single-origins'
data = scrape_coffee_data(url)
df = pd.DataFrame(data)
print(df)
