from user_books import set_url_params
from format_data import (
    format_ratings, 
    save_to_csv, 
    combine_unqiue_list
)
from generic_book import (
    get_generic_book_data, 
    fetch_book_data_from_isbn13, 
    get_books_from_blogpost, 
    get_category_url_choiceawards, 
    get_bookid_from_choiceawards_category_url
)
from bestseller import set_parameters, retrieve_best_sellers
from config import USER_ID

# TODO: 
# 2. Get publisher (if exists)
# 3. Fix better error handling

# Set this to True if we are to collect NYT Best sellers top 100
# Requires NYT API key to be set in config.py
getNYbooks = True

# Set this to True if we are to collect choice awards books. Set the url in the function!
getChoice = True
# Set this to True if we are to collect books from blogpost, ie. Anticipated books. Set the url in the function!
getBlogpost = True

# Here we get a dataframe with objects representing information about the books
books_read = set_url_params(USER_ID,'read')
books_to_read = set_url_params(USER_ID,'to-read')

# Combine the lists
print('Getting books from Goodreads')
for book in books_read:
    book.set_bookshelf('read')
for book in books_to_read:
    book.set_bookshelf('to-read')
all_books = books_read + books_to_read

# Add the generic book-data to the dataframe
# Adds genre, year published and page number
all_books = get_generic_book_data(all_books)

# Format the ratings to numbers
all_books = format_ratings(all_books)

#If getting NYT best sellers
if(getNYbooks == True):
   print('Getting NYT best sellers')
   nyt_url = set_parameters()
   nyt_books = retrieve_best_sellers(nyt_url)
   nyt_books = fetch_book_data_from_isbn13(nyt_books)
   nyt_books = get_generic_book_data(nyt_books)

   # TODO
   # Fix this function, remove, rewrite?
   all_books = combine_unqiue_list(all_books, nyt_books)

if(getChoice == True):
   print('Getting choice awards')
   choice_awards_url = get_category_url_choiceawards()
   choice_books = get_bookid_from_choiceawards_category_url(choice_awards_url)
   choice_books = get_generic_book_data(choice_books)
   all_books = combine_unqiue_list(all_books, choice_books)

if(getBlogpost == True):
   print('Getting blogpost')
   blog_book = get_books_from_blogpost()
   blog_book = get_generic_book_data(blog_book)
   all_books = combine_unqiue_list(all_books, blog_book)
   

#Save to CSV
save_to_csv(all_books)
