import requests
from bs4 import BeautifulSoup
from book import Book

# This file is to fetch books from a Goodreads choice awards page
def get_category_url_choiceawards():
    choice_books_url = 'https://www.goodreads.com/choiceawards/best-books-2023'
    base_url = 'https://www.goodreads.com/'
    page = requests.get(choice_books_url)
    all_urls = []

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        category_div = soup.find_all('div', class_='category clearFix')
        for category_div in category_div:
            # Find all <a> tags within each <div>
            link_tags = category_div.find_all('a')
            for link_tag in link_tags:
                if 'href' in link_tag.attrs and link_tag['href']!='#':
                    url = link_tag['href']
                    all_urls.append(base_url+url)
    return all_urls

def get_bookid_from_category_url(urls):
    all_book_id = []
    for url in urls:
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            # Use a dictionary to match the 'data-resource-id' attribute
            all_books = soup.find_all('div', {'data-resource-id': True, 'class': 'js-tooltipTrigger tooltipTrigger'})
            
            for book in all_books:
                book_id = book['data-resource-id']
                all_book_id.append(book_id)
                print(book_id)

all_urls = get_category_url_choiceawards()
get_bookid_from_category_url(all_urls)

#all_books = get_generic_book_data(all_books)

#all_books = format_ratings(all_books)

#print(all_books)
#for b in all_books:
#    print(b)