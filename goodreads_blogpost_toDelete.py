import requests
from bs4 import BeautifulSoup
import re
from generic_book import get_generic_book_data
from book import Book
from format_data import format_ratings

# This is to fetch books from a Goodreads blog post

def get_book_from_blogpost():
    """
    Retrieves books from a blog post and returns a list of Book objects.

    Returns:
        list: A list of Book objects containing book_id, title, author, and bookshelf.
    """
    anticipated_books_url = 'https://www.goodreads.com/blog/show/2673-goodreads-members-most-anticipated-books-of-2024?ref=MA24_eb'
    page = requests.get(anticipated_books_url)

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
                    title = title_match.group('Title').strip()
                    author = title_match.group('Author').strip()
                    
                    b = Book(
                        book_id=book_id,
                        title=title,
                        author=author,
                        bookshelf='Anticipated'
                    )
                    all_books.append(b)

    return all_books


