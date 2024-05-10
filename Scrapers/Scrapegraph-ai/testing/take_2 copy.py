import os
import datetime
from urllib.parse import urlparse
from scrapegraphai.graphs import SmartScraperGraph
from parse_and_save_test import parse_and_save_data

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

graph_config = {
    "llm": {
        "api_key": OPENAI_API_KEY,
        "model": "gpt-3.5-turbo",
    },
}

# Step 1: Prompt to get the product names and URLs
# Step 1: Scrape the main page to get the product names and URLs
main_page_url = "https://onyxcoffeelab.com/collections/coffee/"
base_product_url = "https://onyxcoffeelab.com/products/"
roaster = urlparse(main_page_url).netloc.split('.')[0]

main_page_prompt = """
Please scroll down to ensure all information is loaded, then list all the product names and URLs listed on the webpage.
- Name: The name of the product
- URL: Using the list of product names along with the base product URL, create the product page URL. The task is to generate a list where each entry includes the product name and its corresponding URL, formed by appending the product name to the base URL.\n\nFor example:\n\nBase URL: {base_product_url}\nProduct Name: Peru La Margarita Gesha\n\nThe output URL should be: {base_product_url}Peru-La-Margarita-Gesha
"""

main_page_graph = SmartScraperGraph(
    prompt=main_page_prompt,
    source=main_page_url,
    config=graph_config
)

# Run the smart scraper graph to get the product names and URLs
main_page_result = main_page_graph.run()

print(main_page_result)

# Extract product names and URLs
products_info = [{'Name': item['Name'], 'URL': base_product_url + item['Name'].replace(" ", "-")} for item in main_page_result.get('products', [])]

# Print product names and URLs before proceeding to Step 2
for product_info in products_info:
    print(f"Product Name: {product_info['Name']}, URL: {product_info['URL']}")

# Step 2: Iterate through each product URL to extract additional details
for product_info in products_info:
    product_name = product_info['Name']
    product_url = product_info['URL']

    # Prompt for scraping product page
    product_page_prompt = f"""
    Please scroll down to ensure all information is loaded and provide details of the product '{product_name}' including the following attributes, provide N/A for a value when that data isn't available:
    - Name: "{product_name}"
    - Description: "N/A"
    - Price: "N/A"
    - Roast Profile Level: "N/A"
    - Cup: "N/A"
    - Origin: "N/A"
    - Process: "N/A"
    - Elevation: "N/A"
    - Variety: "N/A"
    - Story: "N/A"
    - BrewGuides: "N/A"
    """

    product_page_graph = SmartScraperGraph(
        prompt=product_page_prompt,
        source=product_url,
        config=graph_config
    )

    # Run the smart scraper graph to get details of the product
    product_page_result = product_page_graph.run()

    # Print the product details
    print("Product Details:")
    print(product_page_result)
