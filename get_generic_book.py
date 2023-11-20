import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

#####################################################
## This file is to get book-data from the          ##
## generic book-page on Goodreads. Books from user ##
## is collected in file get_user_books.py          ##
#####################################################


def fetch_book_data(book_id): 
    base_url = 'https://www.goodreads.com/book/show/'
    book_url = f'{base_url}{book_id}'
    page = requests.get(book_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Extract genres
    genre_links = soup.select('a[href*="/genres/"]')
    book_genres = [link.text.strip() for link in genre_links]

    # Extract published year and number of pages
    publication_info_element = soup.find('p', {'data-testid': 'publicationInfo'})
    year_published = None
    if publication_info_element:
        publication_info_text = publication_info_element.text.strip()
        year_published = int(publication_info_text.split()[-1]) if publication_info_text else None

    pages_element = soup.find('p', {'data-testid': 'pagesFormat'})
    pages_text = pages_element.text.strip() if pages_element else ''

    try:
        number_of_pages = int(pages_text.split()[0])
    except (ValueError, IndexError):
        number_of_pages = None

    # Join genres into a comma-separated string
    genres_string = ', '.join(book_genres)

    return {'Number_of_Pages': number_of_pages, 'Year_Published': year_published, 'Genres': genres_string}

def get_generic_book_data(booklist): # Initiate the fetching of book-data
    book_ids = booklist['Book_Id'].tolist()
    with ThreadPoolExecutor(max_workers=8) as executor: 
        results = list(executor.map(fetch_book_data, book_ids))

    additional_info = pd.DataFrame(results)
    booklist = pd.concat([booklist, additional_info], axis=1)

    return booklist