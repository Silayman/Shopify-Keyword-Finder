import requests
from bs4 import BeautifulSoup as bs
import time, timeit

def shopify_keywords():
    print(
    """
    Site options (feel free to try other shopify sites):
    cncpts
    bdgastore
    us.bape


    """)
    site = input("Please choose a site: ")
    keyword = input("Please enter keywords: ").lower()
    keywords = keyword.split()
    print(keywords)
    session = requests.session()
    url = "https://{}.com/sitemap_products_1.xml?".format(site)
    response = session.get(url)
    soup = bs(response.content, 'html.parser')
    all_found_urls = []
    for urls_found in soup.find_all("url"):
        for keyword_search in urls_found.find_all("image:image"):
            if all(i in keyword_search.find("image:title").text.lower() for i in keywords):
                print("Matched keywords! -> " + keyword_search.find("image:title").text)
                found_url = "Found URL: " + urls_found.find("loc").text
                all_found_urls.append(urls_found.find("loc").text + ".xml")
                print(found_url)
    for found_products in all_found_urls:
        response = session.get(found_products)
        soup = bs(response.content, 'html.parser')
        ProductName1 = soup.find('hash')
        ProductName = ProductName1.find('title').text
        TagsOfProduct = soup.find('tags').text
        print("-----------------------------------------------------")
        print("Product name: " + str(ProductName) + ". Tags: " + str(TagsOfProduct))
        print("-----------------------------------------------------")
        for variants in soup.find_all('variant'):
            size_id = variants.find('id', {'type': 'integer'}).text
            shoe_size = variants.find('title').text
            shoe_stock = variants.find('inventory-quantity', {"type": "integer"}).text
                        ####shoe_price
            print("Size: " + shoe_size + ". ID: " + size_id + ". Stock: " + shoe_stock)
            if int(shoe_stock) >= 1:
                print("ATC LINK: " + "https://" + str(site) + ".com/cart/" + size_id + ":" + "1")

shopify_keywords()





