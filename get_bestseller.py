from config import NYT_KEY
import requests

# Set the parameters to get books from New York Times Best Seller List
def set_parameters(): 
    base_nyt_url = 'https://api.nytimes.com/svc/books/v3/lists/full-overview.json'
    nyt_url = f'{base_nyt_url}?api-key={NYT_KEY}'
    return nyt_url

# Get the books from the API
def get_books(nyt_url):
    best_sellers = []
    response = requests.get(nyt_url)
    if response.status_code == 200:  # Check so status is 200
        data = response.json()
        for document in data['results']['lists']:  # Nestle down in the API
            book_info = document.get('books', [])  # Get the book data
            for b in book_info:
                # Save some data from the NYT API
                best_sellers.append([b.get('primary_isbn13'), b.get('title').title(), b.get('author')])
    return best_sellers[:100] # Return only 100 first books