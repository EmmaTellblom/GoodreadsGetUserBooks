import pandas as pd
import numpy as np

# Fix the rating-text to numbers
def format_ratings(book_data):
    choices = [5, 4, 3, 2, 1]
    for book in book_data:
        conditions = [
            (book.get_user_rating() == 'it was amazing'),
            (book.get_user_rating() == 'really liked it'),
            (book.get_user_rating() == 'liked it'),
            (book.get_user_rating() == 'it was ok'),
            (book.get_user_rating() == 'did not like it')
        ]
        book.set_user_rating(np.select(conditions, choices, default=''))
    return book_data

def combine_unqiue_list(all_books, new_list):
    """
    Combine unique books from two lists and return the combined list.

    Args:
        all_books (list): A list of all books.
        new_list (list): A new list of books to be combined.

    Returns:
        list: A combined list of unique books from all_books and new_list.
    """
    unique_book_ids = set()

    for book in all_books:
        unique_book_ids.add(book.get_book_id())

    # Iterate through bestseller and add unique books to the list
    unique_new_list = [best for best in new_list if best.get_book_id() not in unique_book_ids]

    # Combine the list
    books_all_shelves = all_books + unique_new_list
    return books_all_shelves

def save_to_csv(book_list):
    columns = [
        'Book_Id', 'Book_Title', 'Author', 'Author_l-f', 'Additional_Authors', 'ISBN', 'ISBN13',
        'My_Rating', 'Average_Rating', 'Publisher', 'Binding', 'Number_of_Pages', 'Year_Published',
        'Original_Publication_Year', 'Date_Read', 'Date_Added', 'Bookshelves',
        'Bookshelves_with_positions', 'Exclusive_Shelf', 'My_Review', 'Spoiler', 'Private_Notes',
        'Read_Count', 'Owned_Copies', 'Genres'
    ]

    rows = []
    for b in book_list:
        row = {
            'Book_Id': b.get_book_id(),
            'Book_Title': b.get_title(),
            'Author': b.get_author(),
            'Author_l-f': '',
            'Additional_Authors': '',
            'ISBN': '',
            'ISBN13': b.get_isbn(),
            'My_Rating': b.get_user_rating(),
            'Average_Rating': b.get_avg_rating(),
            'Publisher': '',
            'Binding': '',
            'Number_of_Pages': b.get_pages(),
            'Year_Published': b.get_year(),
            'Original_Publication_Year': '',
            'Date_Read': '',
            'Date_Added': '',
            'Bookshelves': '',
            'Bookshelves_with_positions': '',
            'Exclusive_Shelf': b.get_bookshelf(),
            'My_Review': '',
            'Spoiler': '',
            'Private_Notes': '',
            'Read_Count': '',
            'Owned_Copies': '',
            'Genres': b.get_genres()
        }
        rows.append(row)

    goodreads_format = pd.DataFrame(rows, columns=columns)
    goodreads_format.to_csv('goodreads_export_with_genres.csv', encoding='utf-8', sep=',', index=False)
