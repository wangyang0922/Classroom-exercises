import requests
from bs4 import BeautifulSoup

url = 'https://beijing.anjuke.com/sale/p1'
html = requests.get(url, timeout=10)
content = html.text
soup = BeautifulSoup(content, 'html.parser', from_encoding='_utf-8')

house_list = soup.find_all('li', class_="list-item")

for house in house_list:
    name = house.find('div', class_="house-title").a.text.strip()
    details = house.find('div', class_="details-item").text.strip()
    address = house.find('span', class_="comm-address").text.strip()
    print(address)