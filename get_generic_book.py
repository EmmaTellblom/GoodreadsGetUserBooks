import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import json

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

# This function is used for getting Goodreads book data from the ISBN13 gotten from NYT API
def fetch_book_data_from_isbn13(book_list):
    book_df = pd.DataFrame(columns=['Book_Id', 'Book_Title', 'Author', 'Year_Published', 'Exclusive_Shelf', 'Average_Rating','Number_of_Pages', 'Genres'])
    base_url = 'https://www.goodreads.com/search?q='
    for b in book_list:
        isbn13_url = f'{base_url}{b[0]}' # ISBN from the booklist
        print(isbn13_url)
        page = requests.get(isbn13_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Get the book_id
        final_url = page.url # Redirected url
        parsed_url = urlparse(final_url)
        path_segments = parsed_url.path.split('/')
        book_id = path_segments[-1] # The book ID is at the back of the url
        book_id = book_id.split('-')[0] # Remove the text after the book_id

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
        # Get average rating from the json-string, expand to other variables later
        script_tag = soup.find('script', {'type': 'application/ld+json'})
        json_data = script_tag.string
        book_data = json.loads(json_data)
        average_rating = book_data['aggregateRating']['ratingValue']

        # Save to DF
        book_df.loc[len(book_df)] = {'Book_Id': book_id, 'Book_Title': b[1],'Author': b[2], 'Year_Published': year_published, 
                                     'Exclusive_Shelf': 'best-seller', 'Average_Rating': average_rating,'Number_of_Pages': number_of_pages, 
                                     'Genres': genres_string}

    return book_df