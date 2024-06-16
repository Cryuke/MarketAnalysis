import requests
from bs4 import BeautifulSoup
import csv

# URL of the website to scrape
URL = 'http://books.toscrape.com/'

# Function to fetch the webpage
def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to parse the HTML and extract book information
def parse_books(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    books = []
    for article in soup.find_all('article', class_='product_pod'):
        title = article.h3.a['title']
        price = article.find('p', class_='price_color').text
        books.append({'title': title, 'price': price})
    return books

# Function to save the book information to a CSV file
def save_to_csv(books, filename='books.csv'):
    keys = books[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(books)

def main():
    # Fetch the webpage
    page_content = fetch_page(URL)
    if page_content:
        # Parse the HTML and extract book information
        books = parse_books(page_content)
        # Save the book information to a CSV file
        save_to_csv(books)
        print(f'Successfully saved {len(books)} books to books.csv')
        # Print the extracted data to the console
        for book in books:
            print(f"Title: {book['title']}, Price: {book['price']}")
    else:
        print('Failed to retrieve the page')

if __name__ == '__main__':
    main()
