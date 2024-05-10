import requests

def save_html_locally(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print("HTML content saved locally.")
    else:
        print("Failed to fetch data from the website.")

if __name__ == "__main__":
    url = 'https://onyxcoffeelab.com/products/Peru-La-Margarita-Gesha'
    file_path = 'onyx_product_example.html'
    save_html_locally(url, file_path)
