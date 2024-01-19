from get_user_books import set_url_params
from format_data import create_combined_list, format_ratings, save_to_csv, combine_bestseller_total
from get_generic_book import get_generic_book_data, fetch_book_data_from_isbn13
from get_bestseller import set_parameters, retrieve_best_sellers
from config import USER_ID

# Set this to True if we are to collect NYT Best sellers top 100
# Adds the NYT books to the export formatted like goodreads books
getNYbooks = True

# Here we get a dataframe with objects representing information about the books
books_read = set_url_params(USER_ID,'read')
books_to_read = set_url_params(USER_ID,'to-read')

# Create a combined dataframe with the books
all_books = create_combined_list(books_read, books_to_read)

# Format the ratings to numbers
all_books = format_ratings(all_books)

# Add the generic book-data to the dataframe
# Adds genre, year published and page number
all_books = get_generic_book_data(all_books)

#If getting NYT best sellers
if(getNYbooks==True):
   #print('Getting NYT best sellers')
   nyt_url = set_parameters()
   nyt_books = retrieve_best_sellers(nyt_url)
   nyt_books = fetch_book_data_from_isbn13(nyt_books)
   all_books = combine_bestseller_total(all_books, nyt_books)
    
#Save to CSV
save_to_csv(all_books)
