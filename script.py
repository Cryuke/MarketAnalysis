import requests
import csv
from bs4 import BeautifulSoup

def extract_strings(elements):
    items = []
    for e in elements:
        items.append(e.string.strip())
    return items

def load_data(file_name, headers, titles):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for title in titles:
            row = [title]
            writer.writerow(row)

def main():
    url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #this exctract the details i want using the soup.seelct ()
    product_page_url = url
    upc = soup.select_one('tr:nth-child(1)').get_text(strip=True)
    title = soup.select_one('#content_inner h1').get_text(strip=True)
    price_excl_tax= soup.select_one ()
    
        #this is how it's going to be shown in my CVS
    headers = ["product_page_url", "universal_product_code", "book_title"]
    titles = [product_page_url, upc, title]
    
    load_data("books_data.csv", headers, titles)

if __name__ == "__main__":
    main()