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

# Step 1: Scrape the main page to get the product names and URLs
main_page_url = "https://onyxcoffeelab.com/collections/coffee/"
roaster = urlparse(main_page_url).netloc.split('.')[0]

main_page_prompt = """
Please list all the product names and URLs listed on the webpage.
- Name: The name of the product
- URL: The URL of the product
"""

main_page_graph = SmartScraperGraph(
    prompt=main_page_prompt,
    source=main_page_url,
    config=graph_config
)

# Run the smart scraper graph to get the product names and URLs
main_page_result = main_page_graph.run()

# Extract product names and URLs from the main page result
products_info = main_page_result['products']

# Print product names and URLs before proceeding to Step 2
for product_info in products_info:
    print(f"Product Name: {product_info['Name']},{product_info['URL']}")

# Step 2: Iterate through each product URL to extract additional details
for product_info in products_info:
    product_name = product_info['Name']
    product_url = product_info['URL']

    # Prompt for scraping product page
    product_page_prompt = f"""
    Please provide details of the product '{product_name}' including the following attributes, provide N/A for a value when that data isn't available:
    - Name: The name of the product
    - Price: The price of the product
    - Roast Type: The type of roast indicated in the roast profiel and "Level:" value on the site, if applicable
    - Tasting Notes: Any tasting notes associated with the product, on website this is called cup
    - Origin: The origin of the coffee
    - Process: The processing method of the coffee
    - Elevation: The elevation at which the coffee is grown
    """

    product_page_graph = SmartScraperGraph(
        prompt=product_page_prompt,
        source=product_url,
        config=graph_config
    )

    # Run the smart scraper graph to get details of the product
    product_page_result = product_page_graph.run()

    # Check if 'products' key exists in the result
    if 'products' in product_page_result:
        product_details = product_page_result['products'][0]
        # Call the parsing function to parse and save the data
        parse_and_save_data(product_details, roaster)
    else:
        print(f"No product details found for '{product_name}'.")

