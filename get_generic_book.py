import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import json

# This add data such as number of pages and published year and
# genres to a book.

#####################################################
## This file is to get book-data from the          ##
## generic book-page on Goodreads. Books from user ##
## is collected in file get_user_books.py          ##
#####################################################

def fetch_book_data(book): 
    """
    Fetches book data for a given book ID.

    Parameters:
        book_id (str): The ID of the book to fetch data for.

    Returns:
        dict: A dictionary containing the following book data:
            - 'Number_of_Pages': The number of pages in the book.
            - 'Year_Published': The year the book was published.
            - 'Genres': A comma-separated string of genres associated with the book.
    """
    base_url = 'https://www.goodreads.com/book/show/'
    book_url = f'{base_url}{book.get_book_id()}'
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
    book.set_pages(number_of_pages)
    book.set_year(year_published)
    book.set_genres(genres_string)

# TODO: Fix for object instead ?
def get_generic_book_data(all_books): # Initiate the fetching of book-data
    with ThreadPoolExecutor(max_workers=8) as executor: 
        list(executor.map(fetch_book_data, all_books))
    return all_books

# This function is used for getting Goodreads book data from the ISBN13 gotten from NYT API
def fetch_book_data_from_isbn13(book_list):
    """
    Fetches book data from Goodreads using a list of book ISBN-13s.

    :param book_list: A list of Book objects containing ISBN-13s.
    :return: The updated list of Book objects with additional data fetched from Goodreads.
    """
    base_url = 'https://www.goodreads.com/search?q='

    for b in book_list:
        isbn13_url = f'{base_url}{b.get_isbn()}' # ISBN from the booklist
        page = requests.get(isbn13_url)
        soup = BeautifulSoup(page.content, 'html.parser')
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

        # Set book data
        b.set_book_id(book_id)
        b.set_pages(number_of_pages)
        b.set_year(year_published)
        b.set_genres(genres_string)
        b.set_avg_rating(average_rating)

    return book_list