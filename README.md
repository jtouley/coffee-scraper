# coffee data scraper

## Overview
The Coffee Data Scraper is a Python-based tool designed to automate the extraction of detailed coffee product information from online roasters' websites. This project initially targets Counter Culture Coffee as a proof of concept (PoC) but is structured to be extendable to additional coffee roasters.

## Purpose
The goal of this scraper is to collect structured data about coffee offerings, including prices, roast types, tasting notes, and origins. This data is crucial for coffee enthusiasts and professionals who track coffee varieties, compare options, and analyze trends in the coffee market.

## Features
- Dynamic Data Extraction: Extracts coffee name, price, roast type, tasting notes, and origin.
- Extendability: Designed with scalability in mind, allowing for easy expansion to scrape data from other coffee roaster websites.
- Output to Structured Format: Saves the scraped data into a well-organized flat file for easy integration with databases or other applications.

## How It Works
The scraper utilizes Python libraries such as requests for fetching web pages and BeautifulSoup for parsing HTML content. For pages loaded dynamically with JavaScript, Selenium is used to render the page content as seen in a web browser.

## Getting Started
### Prerequisites
- Python 3.x
- pip
- Virtual environment (recommended)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourgithubusername/coffee-scraper.git
    ```
2. Navigate to the project directory:
    ```bash
    cd coffee-scraper
    ```
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Usage
Run the scraper using the following command:
```bash
python scraper.py
```
The output will be saved to the data directory as a text file named according to the target roaster and the date of scraping.

## Contributing
Contributions to expand the capabilities of this scraper to include more roasters are welcome. Please fork the project, make your changes, and submit a pull request.

## License
This project is released under the MIT License. See the LICENSE file for more details.
