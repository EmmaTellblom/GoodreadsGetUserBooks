import pandas as pd
import numpy as np

def format_ratings(book_data):
    conditions = [
        (book_data['user_rating'] == 'it was amazing'),
        (book_data['user_rating'] == 'really liked it'),
        (book_data['user_rating'] == 'liked it'),
        (book_data['user_rating'] == 'it was ok'),
        (book_data['user_rating'] == 'did not like it')
    ]

    choices = [5, 4, 3, 2, 1]

    # Update the bookratings to numbers
    book_data['user_rating'] = np.select(conditions, choices, default=None)
    
    return book_data

def create_combined_list(books_have_read, books_to_read):
    books_have_read['bookshelf'] = 'read'
    books_to_read['bookshelf'] = 'to-read'
    books_all_shelves = pd.concat([books_have_read, books_to_read], ignore_index=True)
    return books_all_shelves

def save_to_csv(book_data):
    book_data.to_csv('goodreads_python_export.csv', sep=';')