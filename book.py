class Book:
        
    def __init__(self, title = '', author = '', isbn = '', book_id = '',  year='', pages='', genres='', bookshelf='', user_rating = '', avg_rating = '', description=''):
        """
        Initializes a new instance of the Book class.

        Parameters:
            book_id (int): The unique identifier of the book.
            title (str): The title of the book.
            author (str): The author of the book.
            year (int): The year the book was published.
            pages (int): The number of pages in the book.
            genre (str): The genres of the book.
            bookshelf (str): The bookshelf where the book is located.

        Returns:
            None
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.pages = pages
        self.genres = genres
        self.bookshelf = bookshelf
        self.user_rating = user_rating
        self.avg_rating = avg_rating
        self.description = description

    def get_book_id(self) -> int:
        """Returns The ID of the book."""
        return self.book_id
    def get_isbn(self) -> int:
        """Return The ISBN of the book."""
        return self.isbn
    def get_title(self) -> str:
        """Return the title of the book."""
        return self.title

    def get_author(self) -> str:
        """Return the author of the book. """
        return self.author

    def get_year(self) -> int:
        """Return The year of publication of the book."""
        return self.year

    def get_pages(self) -> int:
        """Return The number of pages in the book."""
        return self.pages

    def get_genres(self) -> str:
        """Return The genres of the book."""
        return self.genres

    def get_bookshelf(self) -> str:
        """Return The bookshelf where the book is located. """
        return self.bookshelf
    
    def get_user_rating(self) -> int:
        """Return The user rating of the book."""
        return self.user_rating
    
    def get_avg_rating(self) -> float:
        """Return The average rating of the book."""
        return self.avg_rating
    
    def get_description(self) -> str:
        """Return The description of the book."""
        return self.description

    def set_pages(self, pages):
        """
        Set the number of pages in the book.

        Parameters:
            pages (int): The number of pages in the book.

        Returns:
            None
        """
        self.pages = pages

    def set_genres(self, genres):
        """
        Set the genres of the book.

        Parameters:
            genres (str): The genres of the book.

        Returns:
            None
        """
        self.genres = genres
    
    def set_book_id(self, book_id):
        """
        Set the ID of the book.

        Parameters:
            book_id (int): The ID of the book.

        Returns:
            None
        """
        self.book_id = book_id
    
    def set_user_rating(self, user_rating = ''):
        """
        Set the user rating of the book.

        Parameters:
            user_rating (int): The user rating of the book.

        Returns:
            None
        """
        self.user_rating = user_rating

    def set_bookshelf(self, bookshelf):
        """
        Set the bookshelf where the book is located.

        Parameters:
            bookshelf (str): The bookshelf where the book is located.

        Returns:
            None
        """
        self.bookshelf = bookshelf

    def set_year(self, year):
        """
        Set the year of publication of the book.

        Parameters:
            year (int): The year of publication of the book.

        Returns:
            None
        """
        self.year = year

    def set_avg_rating(self, avg_rating):
        """
        Set the average rating of the book.

        Parameters:
            avg_rating (float): The average rating of the book.

        Returns:
            None
        """
        self.avg_rating = avg_rating

    def set_description(self, description):
        """
        Set the description of the book.

        Parameters:
            description (str): The description of the book.

        Returns:
            None
        """
        self.description = description
    
    def set_author(self, author):
        """
        Set the author of the book.

        Parameters:
            author (str): The author of the book.

        Returns:
            None
        """
        self.author = author

    def set_title(self, title):
        """
        Set the title of the book.

        Parameters:
            title (str): The title of the book.

        Returns:
            None
        """
        self.title = title
    
    def set_isbn(self, isbn):
        """
        Set the ISBN of the book.

        Parameters:
            isbn (int): The ISBN of the book.

        Returns:
            None
        """
        self.isbn = isbn

    def __str__(self):
        return f"""
        Title: {self.title}
        ISBN: {self.isbn}
        Author: {self.author}
        Year: {self.year}
        Pages: {self.pages}
        Genres: {self.genres}
        Bookshelf: {self.bookshelf}
        User Rating: {self.user_rating}
        Avg Rating: {self.avg_rating}
        Description: {self.description}
        """
