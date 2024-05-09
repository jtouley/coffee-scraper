import requests

url = 'https://counterculturecoffee.com/collections/single-origins'
response = requests.get(url)
print("Status Code:", response.status_code)
print("Content Length:", len(response.text))

if response.status_code == 200:
    print(response.text[:5000000])  # Prints the first 500 characters of the HTML
else:
    print("Failed to fetch data from the website.")
