import requests
import csv
from bs4 import BeautifulSoup
product_urls = []
def extract_strings(elements):
    items = []
    for e in elements:
        items.append(e.string.strip())
    return items
def save_data(file_name, headers, row):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
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
    price_excl_tax = soup.select_one ('tr:nth-child(3) > td').get_text(strip=True)
    price_incl_tax = soup.select_one ('tr:nth-child(4) > td' ).get_text(strip=True)
    quantity_available = soup.select_one ('tr:nth-child(6) > td').get_text(strip=True)
    product_description = soup.select_one ('article > p').get_text(strip=True).replace(',', ';')
    category = soup.select_one ('li:nth-child(3) > a').get_text(strip=True)
    review_rating = soup.select_one ('.star-rating')['class'][1]
    image_tag = soup.select_one('img')['src']


    row = [product_page_url, upc, title, price_excl_tax, price_incl_tax,
           quantity_available, product_description, category, review_rating, image_tag]
    return row
def find_all_category_urls(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    category_links = [a['href'] for a in soup.select('.side_categories ul ul a')]
    return category_links
def get_all_product_url_from_category(url):

    book_details_list = []
    has_next_button = True
 #create product variable  
    while has_next_button:
        #print(f"Processing URL: {url}")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
 #grab all product urls from this page and add it to product url variable 
        book_links_found = [a['href'] for a in soup.select('article > h3 > a')]
        print(f"Found book links: {book_links_found}")
        for book_link in book_links_found:
            book_url = "https://books.toscrape.com/catalogue/" + book_link
            book_url = book_url.replace("/../../../", "/")
            product_urls.append(book_url)
            print(f"Found book URL: {book_url}")
            # Call pulling_single_page_details for each book URL
            details = pulling_single_page_details(book_url)
            book_details_list.append(details)
        next_button = soup.select_one('li.next a')
        if next_button:
            next_page_url = next_button['href']
            base_url = url.rsplit('/', 1)[0]
            url = base_url + '/' + next_page_url
            print(f"Moving to next page: {url}")
        else:
            print("No more pages.")
            has_next_button = False
    return book_details_list 
    #retuen the product urls

def process_product_urls(product_urls):
    rows = []  
    for product_url in product_urls:
        book_details = pulling_single_page_details(product_url) 
        rows.append(book_details) 
    return rows  


def main():
    url = "https://books.toscrape.com/index.html"
    base_url = "https://books.toscrape.com/"
    headers = [
        "product_page_url", "universal_product_code", "book_title", "price_excl_tax",
        "price_incl_tax", "quantity_available", "product_description", "category",
        "review_rating", "image_url"
    ]
    
    # Step 1: Find all category URLs
    print("Fetching category URLs...")
    category_links_found = find_all_category_urls(url)
    print(f"Category URLs found: {category_links_found}")

    # Construct full category URLs
    full_category_urls = [base_url + link for link in category_links_found]
    print(f"Full category URLs: {full_category_urls}")

    # Step 2: Gather all product URLs from all categories
    all_product_urls = []
    for full_category_url in full_category_urls:
        print(f"Processing category URL: {full_category_url}")
        product_urls = get_all_product_url_from_category(full_category_url)  # Pass full_category_url
        all_product_urls.extend(product_urls)
    
    print(f"All product URLs collected: {all_product_urls}")

    # Step 3: Pull details for all products
    book_details_list = []
    for product_url in all_product_urls:
        full_product_url = base_url + product_url.lstrip('/')
        print(f"Fetching details for product URL: {full_product_url}")
        product_details = pulling_single_page_details(full_product_url)
        book_details_list.append(product_details)
    
    print(f"Captured book details: {book_details_list}")
    save_data("books_data.csv", headers, book_details_list)

if __name__ == "__main__":
    main()
