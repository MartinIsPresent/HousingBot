import requests
from bs4 import BeautifulSoup

session = requests.Session()
initial_url = 'https://maastrichthousing.com/Search_results.html'
initial_response = session.get(initial_url)

soup = BeautifulSoup(initial_response.text, 'html.parser')
csrf_token_tag = soup.find('meta', attrs={'name': 'csrf-token'})
csrf_token = csrf_token_tag['content'] if csrf_token_tag else None

if not csrf_token:
    print("Could not find CSRF token. Aborting.")
    exit()

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': initial_url,
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRF-Token': csrf_token
}

payload = {
    'housing_corporation': '1',
    'private_market': '1',
    'furnished': 'all',
    'type[]': ['room', 'studio', 'apartment'],
    'surface_min': 0,
    'surface_max': 500,
    'rent_min': 50,
    'rent_max': 3000,
    'i': '1',
    'u': '1',
}
ajax_url = 'https://maastrichthousing.com/ajax-search?page=1'
response = session.post(ajax_url, headers=headers, data=payload)
if response.status_code == 200:
    listings_data = response.json().get('results', [])

    print("\nAvailable Listings:\n" + "-"*60)
    for item in listings_data:
        html = item.get('html', '')
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find('h3', class_='panel-title')
        price = soup.find('div', class_='panel-footer')
        link_tag = soup.find('a', href=True)

        print(f"Title: {title.text.strip() if title else 'N/A'}")
        print(f"Price: {price.text.strip() if price else 'N/A'}")
        print(f"URL: {link_tag['href'] if link_tag else 'N/A'}")
        print("-" * 60)

else:
    print(f"Request failed: {response.status_code}")
    print(response.text)
