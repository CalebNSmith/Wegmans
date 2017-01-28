__author__ = 'Caleb'
import requests
from bs4 import BeautifulSoup

url = "http://www.wegmans.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


for ul in soup.find_all('ul'):
    for li in ul.find_all('li'):
        for href in li.find_all('a'):
            print(href)

