import os
from scrapegraphai.graphs import SmartScraperGraph

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

graph_config = {
    "llm": {
        "api_key": OPENAI_API_KEY,
        "model": "gpt-3.5-turbo",
    },
}

prompt = """
Please provide details of the products listed on the webpage, including the following attributes:
- Name: The name of the product
- Price: The price of the product
- Roast Type: The type of roast, if applicable
- Tasting Notes: Any tasting notes associated with the product
"""

smart_scraper_graph = SmartScraperGraph(
    prompt=prompt,
    source="https://bluebottlecoffee.com/us/eng/collection/single-origin",
    config=graph_config
)

result = smart_scraper_graph.run()
print(result)
