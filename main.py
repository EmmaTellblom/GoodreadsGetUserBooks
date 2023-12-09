from get_user_books import set_url
from format_data import create_combined_list, format_ratings, save_to_csv, combine_bestseller_total
from get_generic_book import get_generic_book_data
from get_bestseller import set_parameters, get_books, fetch_book_data_from_isbn13
from config import USER_ID

# Set this to True if we are to collect NYT Best sellers top 100
# To use for recommending books from the best selling list later
getNYbooks = True

books_read, books_to_read = set_url(USER_ID)

# Create a combined dataframe with the books
all_books = create_combined_list(books_read, books_to_read)

# Format the ratings to numbers
all_books = format_ratings(all_books)

# Add the generic book-data to the dataframe
all_books = get_generic_book_data(all_books)

# If getting NYT best sellers
if(getNYbooks==True):
    print('Getting NYT best sellers')
    nyt_url = set_parameters()
    nyt_books = get_books(nyt_url)
    nyt_books = fetch_book_data_from_isbn13(nyt_books)
    all_books = combine_bestseller_total(all_books, nyt_books)
    
# Save to CSV
save_to_csv(all_books)
