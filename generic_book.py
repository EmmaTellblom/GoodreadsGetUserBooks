import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import json
import re
import html
from book import Book

#####################################################
## This file is to get book-data from the          ##
## generic book-page and/or blog post and/or       ##
## choice awards on Goodreads. Books from user     ##
## is collected in file user_books.py              ##
#####################################################

# TODO:
# Add publisher (if exists)

def fetch_book_data_from_id(book): 
    """
    Fetches book data for a given book based on book_id from the 'generic' book page on Goodreads.
    Requires that a book-object has been created first and passed to this function.

    Parameters:
        book (Book): An instance of the Book class representing the book to fetch data for.

    Returns:
        None
    """
    # Construct the URL for the book
    base_url = 'https://www.goodreads.com/book/show/'
    book_url = f'{base_url}{book.get_book_id()}'

    num_pages = ''
    title = ''
    author = ''
    average_rating = ''
    year_published = ''
    isbn = ''

    # Send a GET request to the book URL
    page = requests.get(book_url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(page.content, 'html.parser')

    # Some info is in json format
    script_tag = soup.find('script', type='application/ld+json')

    if script_tag:
        json_data = script_tag.string
        # Parse the JSON data
        parsed_data = json.loads(html.unescape(json_data))
        
        # Extract the desired fields
        title = parsed_data.get("name", "")
        author = parsed_data.get("author", [{}])[0].get("name", "")
        average_rating = parsed_data.get("aggregateRating", {}).get("ratingValue", "")
        isbn = parsed_data.get("isbn", "")
        num_pages = parsed_data.get("numberOfPages", "")

    # Extract genres
    genre_links = soup.select('a[href*="/genres/"]')
    book_genres = [link.text.strip() for link in genre_links]

    # Extract published year
    publication_info_element = soup.find('p', {'data-testid': 'publicationInfo'})
    year_published = ''
    if publication_info_element:
        publication_info_text = publication_info_element.text.strip()
        year_published = int(publication_info_text.split()[-1]) if publication_info_text else ''

    # Extract description
    description_element = soup.select_one('div.DetailsLayoutRightParagraph__widthConstrained span.Formatted')
    book_description = description_element.text.strip() if description_element else ''

    # Join genres into a comma-separated string
    genres_string = ', '.join(book_genres)

    # Set the book's data
    book.set_pages(num_pages)
    book.set_year(year_published)
    book.set_genres(genres_string)
    book.set_description(book_description)
    book.set_title(title)
    book.set_author(author)
    book.set_isbn(isbn)
    book.set_avg_rating(average_rating)

def get_generic_book_data(all_books): # Initiate the fetching of book-data
    """
	Initiate the fetching of book-data
	"""
    with ThreadPoolExecutor(max_workers=8) as executor: 
        list(executor.map(fetch_book_data_from_id, all_books))
    return all_books

# TODO:
# Fix so this function takes the pagesource and send to generic function
# This function is used for getting Goodreads book data from the ISBN13 gotten from NYT API
def fetch_book_data_from_isbn13(book_list):
    """
    Fetches book data from Goodreads using a list of book objects with ISBN-13.

    :param book_list: A list of Book objects containing ISBN-13s.
    :return: The updated list of Book objects with bookids
    """
    base_url = 'https://www.goodreads.com/search?q='

    for b in book_list:
        isbn13_url = f'{base_url}{b.get_isbn()}' # ISBN from the booklist
        page = requests.get(isbn13_url)
        #soup = BeautifulSoup(page.content, 'html.parser')
        final_url = page.url # Redirected url
        parsed_url = urlparse(final_url)
        path_segments = parsed_url.path.split('/')
        book_id = path_segments[-1] # The book ID is at the back of the url
        book_id = book_id.split('-')[0] # Remove the text after the book_id
        b.set_book_id(book_id)
    return book_list

# TODO:
# Fix so this sends bookids to generic function
def get_books_from_blogpost():
    """
    Retrieves books from a blog post and returns a list of Book objects.

    Returns:
        list: A list of Book objects containing book_id, title, author, and bookshelf.
    """
    # URL to blogpost
    blogpost_url = 'https://www.goodreads.com/blog/show/2673-goodreads-members-most-anticipated-books-of-2024?ref=MA24_eb'
    page = requests.get(blogpost_url)

    all_books = []

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        title_divs = soup.find_all('div', class_='bookTitle')

        book_id_pattern = re.compile(r'/book/show/(\d+)')
        title_author_pattern = re.compile(r'(?P<Title>.+?)\s*by\s*(?P<Author>.+)')
        
        for title_div in title_divs:
            title_text = title_div.text
            title_match = title_author_pattern.search(title_text)
            
            if title_match:
                book_id_match = book_id_pattern.search(title_div.a['href'])
                if book_id_match:
                    book_id = book_id_match.group(1)
                    
                    b = Book(
                        book_id=book_id,
                        bookshelf='blog_post'
                    )
                    all_books.append(b)

    return all_books

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

def get_bookid_from_choiceawards_category_url(urls):
    all_books_list = []
    for url in urls:
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            # Use a dictionary to match the 'data-resource-id' attribute
            all_books = soup.find_all('div', {'data-resource-id': True, 'class': 'js-tooltipTrigger tooltipTrigger'})
            for book in all_books:
                book_id = book['data-resource-id']
                b = Book(
                    book_id=book_id,
                    bookshelf='choice_awards'
                )
                all_books_list.append(b)
    return all_books_list