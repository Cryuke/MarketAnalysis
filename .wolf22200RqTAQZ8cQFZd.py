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

    upc = soup.select_one('tr:nth-child(1)').get_text(strip=True)if soup.find('tr', {'nth-child': '1'}) else 'N/A'
    title = soup.select_one('#content_inner h1').get_text(strip=True)
    price_excl_tax = soup.select_one ('tr:nth-child(3) > td').get_text(strip=True)
    price_incl_tax = soup.select_one ('tr:nth-child(4) > td' ).get_text(strip=True)
    quantity_available = soup.select_one ('tr:nth-child(6) > td').get_text(strip=True)
    product_description = soup.select_one ('article > p').get_text(strip=True).replace(',', ';')
    category = soup.select_one ('li:nth-child(3) > a').get_text(strip=True)
    review_rating = soup.select_one ('.star-rating')['class'][1]
    image_tag = soup.select_one('img')['src']

    print("upc", upc)
   

    row = [product_page_url, upc, title, price_excl_tax, price_incl_tax, 
        quantity_available, product_description, category, review_rating, image_tag]
    return row
def pulling_from_catogoery(url):
    while url:
        # Request the current page
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find all book URLs on the current category page
        book_links = [a['href'] for a in soup.select('.product_pod h3 a')]

        for book_link in book_links:
            book_url = "https://books.toscrape.com/catalogue/" + book_link
            book_details = pulling_single_page_details(book_url)
            rows.append(book_details)

        # Check for the next page
        next_button = soup.select_one('li.next a')
        if next_button:
            next_page_url = next_button['href']
            base_url = url.rsplit('/', 1)[0]
            url = base_url + '/' + next_page_url
        else:
            url = None

    #starting catogoery url: 
    # https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html
    # https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-2.html
    # for each catogoery page until there is no next button
    #  Find each book's url in the catogoery page
    #   Loop through each url in the catogoery
    #    open each url for a book 
    #       pull single page details
    #  return all rows of product details
    
def main():

    url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-2.html"

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