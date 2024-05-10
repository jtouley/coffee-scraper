import os
import datetime
from urllib.parse import urlparse
from scrapegraphai.graphs import SmartScraperGraph
from parse_and_save import parse_and_save_data

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

graph_config = {
    "llm": {
        "api_key": OPENAI_API_KEY,
        "model": "gpt-3.5-turbo",
    },
}

url = "https://bluebottlecoffee.com/us/eng/collection/single-origin"
# Parse the URL to extract the roaster name
roaster = urlparse(url).netloc.split('.')[0]

prompt = """
Please provide details of the products listed on the webpage, including the following attributes:
- Name: The name of the product
- Price: The price of the product
- Roast Type: The type of roast, if applicable
- Tasting Notes: Any tasting notes associated with the product
"""

smart_scraper_graph = SmartScraperGraph(
    prompt = prompt,
    source=url,
    config=graph_config
)

# Run the smart scraper graph and get the result
result = smart_scraper_graph.run()

# Call the universal parsing function to parse and save the data
parse_and_save_data(result, roaster)
