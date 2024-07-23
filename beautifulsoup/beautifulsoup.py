import requests
from bs4 import BeautifulSoup
url = "https://www.gov.uk/search/news-and-communications"
page = requests.get(url)


soup = BeautifulSoup(page.content, 'html.parser')


#print(soup)
titles = soup.find_all("h1", class_="govuk-heading-xl")
print(titles)
