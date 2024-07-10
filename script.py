import requests
import csv
from bs4 import BeautifulSoup

def extract_strings(elements):
    items = []
    for e in elements:
        items.append(e.string.strip())
    return items


def save_data(file_name, headers, row):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(headers)
        for row in row:
        
            writer.writerow(row)



def pulling_single_page_details(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    product_page_url = url

    upc = soup.select_one('tr:nth-child(1)').get_text(strip=True)
    title = soup.select_one('#content_inner h1').get_text(strip=True)
    price_excl_tax= soup.select_one ('tr:nth-child(3) > td').get_text(strip=True)
    price_incl_tax= soup.select_one ('tr:nth-child(4) > td' ).get_text(strip=True)
    quantity_available= soup.select_one ('tr:nth-child(6) > td').get_text(strip=True)
    product_description= soup.select_one ('article > p').get_text(strip=True).replace(',', ';')
    category= soup.select_one ('li:nth-child(3) > a').get_text(strip=True)
    review_rating= soup.select_one ('.star-rating')['class'][1]
    image_tag = soup.select_one('img')['src']


    print("price_excl_tax", price_excl_tax)
    print("price_incld_tax", price_incl_tax)
    print("quantity_available", quantity_available)
    print("category", category)
    print("review_rating", review_rating)
    print("image_tag", image_tag)

    row = [product_page_url, upc, title, price_excl_tax, price_incl_tax, 
        quantity_available, product_description, category, review_rating, image_tag]
    return row


def main():

    url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

    headers = [
        "product_page_url", "universal_product_code", "book_title", "price_excl_tax", 
        "price_incl_tax", "quantity_available", "product_description", "category", 
        "review_rating", "image_url"
    ]
    row = pulling_single_page_details(url)
    rows = [row]
    save_data("books_data.csv", headers, rows)

if __name__ == "__main__":
    main()