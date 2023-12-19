from config import NYT_KEY
import requests

# Set the parameters to get books from New York Times Best Seller List
def set_parameters(): 
    base_nyt_url = 'https://api.nytimes.com/svc/books/v3/lists/current/combined-print-and-e-book-fiction.json'
    nyt_url = f'{base_nyt_url}?api-key={NYT_KEY}'
    return nyt_url

# Get the books from the API
# Returns a list of 15 books on the fiction list
def get_books(nyt_url):
    best_sellers = []
    response = requests.get(nyt_url)
    if response.status_code == 200:
        data = response.json()
        for document in data['results']['books']:  # Nestle down in the API
            best_sellers.append([document.get('primary_isbn13'), document.get('title').title(), document.get('author')])
    return best_sellers

test = set_parameters()
get_books(test)