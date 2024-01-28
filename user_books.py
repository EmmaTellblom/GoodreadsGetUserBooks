import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from book import Book

###################################################
## This file is to get books from user bookshelf ##
## bookshelf. Generic book-data from Book_Id     ##
## is collected in the file get_generic_book.py  ##
## This is needed because user bookshelf is not  ##
## the same as generic book-page in Goodreads    ##
###################################################

def set_url_params(user_id, bookshelf):
    """
    Sets the URLs for the bookshelf to-read and read.

    Parameters:
    user_id (int): The ID of the user.

    Returns:
    tuple: A tuple containing two lists - `books_read` and `books_to_read`.
           `books_read` (dataframe): A list of book objects from the user's read bookshelf.
           `books_to_read` (dataframe): A list of book objects from the user's to-read bookshelf.
    """
    read_books_url = f'https://www.goodreads.com/review/list/{user_id}?&shelf=read'
    to_read_books_url = f'https://www.goodreads.com/review/list/{user_id}?shelf=to-read'
    # Get how many pages there are to paginate
    if(bookshelf == 'read'):
        no_pageinations = get_no_of_paginations(read_books_url)
        url = read_books_url
    else:
        no_pageinations = get_no_of_paginations(to_read_books_url)
        url = to_read_books_url
    books = get_user_book_info(url, no_pageinations)
    return books

    

def get_no_of_paginations(book_url): # Get number of pages needed to paginate through
    """
	Get number of pages needed to paginate through.

	:param book_url: The URL of the book.
	:type book_url: str
	:return: The number of pages needed to paginate through.
	"""
    number_of_books = 0
    page = requests.get(book_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    no_books = soup.find('title')
    if no_books:
        match = re.search(r'\((\d+) books\)', no_books.text) # Text for no books in user bookshelf
        if match:
            number_of_books = int(match.group(1))
    if number_of_books > 30: # Goodreads display 30 per page
        number_of_pages = round(number_of_books/30)
    else:
        number_of_pages = 1
    return number_of_pages # No of pages to paginate

def get_user_book_info(book_url, number_of_pages):
    """
    Retrieves information about books from a given URL.
    
    Args:
        book_url (str): The URL of the page containing the book information.
        number_of_pages (int): The number of pages to scrape.
        
    Returns:
        pandas.DataFrame: A DataFrame containing objects representing information about the books.
    """
    books = []
    for i in range(1, number_of_pages + 1):
        book_url_pages = book_url + f'&page={i}' # Create pagination URL
        page = requests.get(book_url_pages)
        soup = BeautifulSoup(page.content, 'html.parser')
        book_links = soup.select('tr.bookalike.review')

        for link in book_links:
            book_id_match = re.search(r'/book/show/(\d+)', link.find('a', href=True)['href'])
            book = Book(
                book_id = book_id_match.group(1)
            )
            static_stars_element = link.find_next('td', class_='field rating').find('span', class_='staticStars')
            if static_stars_element:
                book.set_user_rating(static_stars_element.get('title'))
            books.append(book)
    return books
    

