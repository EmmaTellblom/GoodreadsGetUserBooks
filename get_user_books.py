import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

###################################################
## This file is to get books from user bookshelf ##
## bookshelf. Generic book-data from Book_Id     ##
## is collected in the file get_generic_book.py  ##
###################################################

def set_url(user_id):
    # Base-urls for the bookshelf to-read and read
    read_books_url = f'https://www.goodreads.com/review/list/{user_id}?&shelf=read'
    to_read_books_url = f'https://www.goodreads.com/review/list/{user_id}?shelf=to-read'
    # Get how many pages there are to paginate
    no_pages_read = get_no_of_pages(read_books_url)
    no_pages_to_read = get_no_of_pages(to_read_books_url)
    # Get book data from user bookshelf
    books_read = get_user_book_info(read_books_url, no_pages_read)
    books_to_read = get_user_book_info(to_read_books_url, no_pages_to_read)
    return books_read,books_to_read

def get_no_of_pages(book_url): # Get number of pages needed to paginate through
    page = requests.get(book_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    no_books = soup.find('title')
    if no_books:
        match = re.search(r'\((\d+) books\)', no_books.text) # Text for no books in user bookshelf
        if match:
            number_of_books = int(match.group(1))
    if number_of_books > 30: # Goodreads display 30 per page
        number_of_pages = round(number_of_books/30)
    else:
        number_of_pages = 1
    return number_of_pages # No of pages to paginate

def get_user_book_info(book_url, number_of_pages):
    books = pd.DataFrame(columns=['Book_Id', 'Book_Title', 'Author','Author_l-f', 'Additional_Authors', 'ISBN', 'ISBN13', 'My_Rating', 'Average_Rating', 'Publisher', 'Binding', 'Number_of_Pages', 'Year_Published', 'Original_Publication_Year', 'Date_Read', 'Date_Added', 'Bookshelves', 'Bookshelves_with_positions', 'Exclusive_Shelf', 'My_Review', 'Spoiler', 'Private_Notes', 'Read_Count', 'Owned_Copies', 'Genres'])
    dataframes = []
    for i in range(1,number_of_pages+1):
        book_url_pages = book_url + f'&page={i}' # Create pagination URL
        page = requests.get(book_url_pages)
        soup = BeautifulSoup(page.content, 'html.parser')   
        book_links = soup.select('a[href*="/book/show/"]')
        book_info = []
        for link in book_links:
            info = {
                'Book_Id': link['href'].split('/')[-1].split('-')[0].split('.')[0],
                'Book_Title': link.get('title'),
                'Author': link.find_next('td', class_='field author').find('a').text.strip().replace('"', ''),
                #'Author': link.find_next('td', class_='field author').find('a').text.strip(),
                'Average_Rating': link.find_next('td', class_='field avg_rating').find('div', class_='value').text.strip(),
            }
            # Check if 'user_rating' element is present
            static_stars_element = link.find_next('td', class_='field rating').find('span', class_='staticStars')
            if static_stars_element:
                info['My_Rating'] = static_stars_element.get('title')  # Get the rating text if rated
            else: # If not rated (might me to-read) set None
                info['My_Rating'] = None
            
            book_info.append(info)

        # Create a DataFrame for the current page and add it to the list
        dataframes.append(pd.DataFrame(book_info, columns=['Book_Id', 'Book_Title', 'Author', 'Average_Rating', 'My_Rating']))

    # Concatenate all DataFrames in the list
    books = pd.concat(dataframes, ignore_index=True)
    print('I have collected user books')
    # Drop rows with None values in the 'title' column becuse of duplicates
    books = books.dropna(subset=['Book_Title'])   
    books = books.reset_index(drop=True)
    return books

