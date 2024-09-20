import requests
from bs4 import BeautifulSoup as BS

link = "https://www.nstu.ru/"
response = requests.get(link).text
soup = BS(response, "lxml")

print(soup.find("div", class_ = "main-events__grid js-main-events-grid").get_text())
# print(soup.get_text())
# for link in soup.find_all('a'):
    # print(link.get('href'))

# print(response.status_code)
# print(response.text)
