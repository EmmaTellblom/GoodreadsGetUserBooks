from get_books import set_url
from config import USER_ID

books_read, books_to_read = set_url(USER_ID)
print(books_read)