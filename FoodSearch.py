__author__ = 'Caleb and Alex'
import requests
from bs4 import BeautifulSoup
import json
import ast
import re

# url = "http://www.wegmans.com"
# response = requests.get(url)
# soup = BeautifulSoup(response.content, "html.parser")
#
#
# for ul in soup.find_all('ul'):
#     for li in ul.find_all('li'):
#         for href in li.find_all('a'):
#             if "/products/" in str(href):
#                 print(href)

def get_category_URLs():
    url = "http://www.wegmans.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    paths = []
    for ul in soup.find_all('ul'):
        for li in ul.find_all('li'):
            for href in li.find_all('a'):
                if "/products/" in str(href):
                    href_string = str(href)
                    href_list = href_string.split('"')
                    paths.append(href_list[1])
    return paths

# for path in paths, we will call this second function
def get_subcategory_URLs(url):
    path = url.replace(".html", "").replace("/products/","")
    categories = []
    try:
        json_url = "https://www.wegmans.com/products/"+ path +"/_jcr_content.department." + path + ".json"
        response = requests.get(json_url)
        for child in response.json():
            categories.append(child['linkUrl'])
    except json.decoder.JSONDecodeError:
        return []
    return categories


# response = requests.get("https://sp1004f27d.guided.ss-omtrdc.net/?do=prod-search;storeNumber=127;q1=Baby%20Formula%20%26%20Electrolytes;x1=cat.category;q2=Baby%20Essentials;x2=cat.department;sp_c=18;sp_n=" + n_cat + ';callback=angular.callbacks._f")'
# soup = BeautifulSoup(response.content, "html.parser")

# paths = get_category_URLs()
# for path in paths:
#     sub_categories = get_subcategory_URLs(path)
#     for sub in sub_categories:
#         products = get_products(sub)
#         for product in products:
#             #get nutritional info/cost/etc.

def get_products(path, store_num):
    splitpath = path.split("/")
    category = splitpath[2]
    subcategory = splitpath[3]
    page_number = 1
    has_more_pages = True
    links = []

    while has_more_pages:
        response = requests.get('https://sp1004f27d.guided.ss-omtrdc.net/?do=prod-search;storeNumber=' + str(store_num) + ';q1=' + subcategory.replace("-", "%20") + ';x1=cat.category;q2=' + category.replace("-", "%20") + ';x2=cat.department;sp_c=18;sp_n=' + str(page_number) + ';callback=angular.callbacks._f')
        output = repr(str(response.content).replace("b'angular.callbacks._f( ", "").replace("\\n", "").replace("\"", "'"))
        start = []
        end = []
        for m in re.finditer("url", output):
            start.append(m.start() + 8)
        for m in re.finditer(".html", output):
            end.append(m.end())
        if len(start) != len(end):
            print(output)
            print(len(start))
            print(len(end))

        for i in range(min(len(start), len(end))):
            links.append(output[start[i] : end[i]])
        start = 0
        for m in re.finditer('resultcount', output):
            start = m.start()
        end = 0
        for m in re.finditer('pageupper', output):
            end = m.end() + 10

        values = []
        for i in output[start:end].split("'"):
            try:
                values.append(int(i))
            except ValueError:
                continue
        if sorted(values)[-1] == sorted(values)[-2]:
            has_more_pages = False
        else:
            page_number += 1
        print(page_number)
    return links
categories = get_category_URLs()
urls = []
for category in categories:
    urls.extend(get_subcategory_URLs(category))
product_links = []
for url in urls:
    product_links.extend(get_products(url, 127))
print(len(product_links))
print(product_links)