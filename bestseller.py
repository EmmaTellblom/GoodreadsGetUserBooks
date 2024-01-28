from config import NYT_KEY
import requests
from book import Book

# Set the parameters to get books from New York Times Best Seller List
def set_parameters(): 
    """
    Generates the URL for the New York Times API endpoint.
    Returns:
        str: The URL for the New York Times API endpoint.
    """
    base_nyt_url = 'https://api.nytimes.com/svc/books/v3/lists/current/combined-print-and-e-book-fiction.json'
    nyt_url = f'{base_nyt_url}?api-key={NYT_KEY}'
    return nyt_url

# Get the books from the API
# Returns a list of 15 books on the fiction list
def retrieve_best_sellers(api_url):
    """
    Retrieves a list of best-selling books from the New York Times API.
    Parameters:
    - api_url (str): The URL of the New York Times API.
    Returns:
    - best_sellers (list): A list of best-selling books. Each book is represented as a list containing the primary ISBN-13, title, and author.
    """
    best_sellers = []
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        for document in data['results']['books']:
            book = Book(
                #title = document.get('title').title(),
                #author = document.get('author'),
                isbn = document.get('primary_isbn13'),
                bookshelf = 'best-seller'
            )
            best_sellers.append(book)
    return best_sellers