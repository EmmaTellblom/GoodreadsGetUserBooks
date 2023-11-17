import pandas as pd
import numpy as np

# Fix the rating-text to numbers
def format_ratings(book_data):
    conditions = [
        (book_data['My_Rating'] == 'it was amazing'),
        (book_data['My_Rating'] == 'really liked it'),
        (book_data['My_Rating'] == 'liked it'),
        (book_data['My_Rating'] == 'it was ok'),
        (book_data['My_Rating'] == 'did not like it')
    ]

    choices = [5, 4, 3, 2, 1]
    book_data['My_Rating'] = np.select(conditions, choices, default=None)

    return book_data

# Put the to-read and read to one dataframe to look like Goodreads export
def create_combined_list(books_have_read, books_to_read): 
    books_have_read['Exclusive_Shelf'] = 'read'
    books_to_read['Exclusive_Shelf'] = 'to-read'
    books_all_shelves = pd.concat([books_have_read, books_to_read], ignore_index=True)
    return books_all_shelves

def save_to_csv(book_data):
    book_data.to_csv('goodreads_python_export.csv', encoding='utf-8', sep=';', index=False)