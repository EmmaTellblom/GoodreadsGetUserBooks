from get_books import set_url
from format_data import create_combined_list, format_ratings, save_to_csv
from config import USER_ID

books_read, books_to_read = set_url(USER_ID)

# Create a combined dataframe with the books
all_books = create_combined_list(books_read, books_to_read)

# Format the ratings to numbers
all_books = format_ratings(all_books)

# Save to CSV
save_to_csv(all_books)
