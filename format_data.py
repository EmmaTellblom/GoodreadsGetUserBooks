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

def combine_bestseller_total(booklist, bestseller):
    # Need to check if there are duplicate book_id in dataframes
    booklist = pd.DataFrame(booklist)
    bestseller = pd.DataFrame(bestseller)
    # Check for duplicates in book_id
    duplicates = pd.merge(booklist[['Book_Id']], bestseller[['Book_Id']], how='inner', on='Book_Id')
    bestseller = bestseller[~bestseller['Book_Id'].isin(duplicates['Book_Id'])]
    # Combine the list
    books_all_shelves = pd.concat([booklist, bestseller], ignore_index=True)
    return books_all_shelves

def save_to_csv(book_data):
    # Add columns to make sure they match goodreads export
    columns_to_include = ['Author_l-f', 'Additional_Authors', 'ISBN', 'ISBN13', 'Publisher', 'Binding', 'Year_Published', 'Original_Publication_Year', 'Date_Read', 'Date_Added', 'Bookshelves', 'Bookshelves_with_positions', 'My_Review', 'Spoiler', 'Private_Notes', 'Read_Count', 'Owned_Copies']
    for col in columns_to_include:
        if col not in book_data.columns:
            book_data[col] = np.nan

    # Arrange columns in the desired order
    desired_order = ['Book_Id', 'Book_Title', 'Author', 'Author_l-f', 'Additional_Authors', 'ISBN', 'ISBN13',
                     'My_Rating', 'Average_Rating', 'Publisher', 'Binding', 'Number_of_Pages', 'Year_Published',
                     'Original_Publication_Year', 'Date_Read', 'Date_Added', 'Bookshelves',
                     'Bookshelves_with_positions', 'Exclusive_Shelf', 'My_Review', 'Spoiler', 'Private_Notes',
                     'Read_Count', 'Owned_Copies', 'Genres']

    # Reorder columns
    ordered_book_data = book_data[desired_order]

    # Save to CSV
    ordered_book_data.to_csv('goodreads_export_with_genres.csv', encoding='utf-8', sep=',', index=False)

def save_to_csv_as_is(booklist):
    booklist = pd.DataFrame(booklist)
    booklist.to_csv('validate_data.csv', encoding='utf-8', sep=',', index=False)