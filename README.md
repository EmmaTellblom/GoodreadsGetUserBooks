# Goodreads User Book Info Scraper
Goodreads User Book Info Scraper
Are you tired of dealing with Goodreads exports or keen on retrieving book information from a particular Goodreads user? Look no further! This script offers a solution. The inspiration behind this project came from a friend who grew weary of sharing Goodreads exports with me.

I use the data gathered by this scraper in conjunction with another repository to predict book ratings, providing my friends with more personalized book recommendations. Why spend time on books that won't captivate you? Say goodbye to post-book hangovers and dive into another fantastic read instead!

## New features!
I have extended this script to get even more data from Goodreads!
* Blog posts (for example the blogpost about most anticipated books for 2024)
* Choice awards

Simply set the url for what blogpost or choice award you want to collect the books from and go! 
This will give you an even bigger chance to find your next great read!

## Integration with NYT Best Sellers List (Requires personal API key)
In addition to retrieving and organizing Goodreads data, this script seamlessly integrates information from the New York Times (NYT) Best Sellers list. By combining insights from both the Goodreads user's reading history and the current best-selling books, the integrated dataset becomes a powerful resource for machine learning applications.

Now, you not only have a personalized view of the books you enjoy but can also explore and discover titles that are trending and recognized as best sellers by the NYT. This holistic approach enhances the accuracy of book recommendations, ensuring a delightful reading experience every time.

## Usage

1. Install the required dependencies:
pip install requests pandas beautifulsoup4 numpy 

Set up your Goodreads user ID in the config_sample.py file and rename to config.py
The userID currently being in the file belongs to a fantastic author, Drew Hayes, you should check him out!
In order for you to use New York Time Best Seller API you need an API-key. This can be retrived from their website: https://developer.nytimes.com/

Run the script:
python main.py

## Functionality
The script fetches book information such as book ID, title, author, average rating, and user rating. It paginates through the user's bookshelf (to-read and read) to collect comprehensive data.

* A specific users read/to-read books
* Choice Awards: Retrieve books from Goodreads Choice Awards. You need to set the URL for the Choice Awards page.
* Blog Posts: Fetch book information mentioned in blog posts. You need to set the URL for the blog post page.
* New York Times Bestsellers: Fetch the most recent top 15 fiction books from New York Times Best Seller list

The exported file can then be used for Machine Learning applications. Such as my R-repo 'BookRatingProphet' which will recommend books based on your history.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
