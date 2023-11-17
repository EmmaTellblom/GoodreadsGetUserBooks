# Goodreads User Book Info Scraper
Are you tired of dealing with Goodreads exports or keen on retrieving book information from a particular Goodreads user? Look no further! This script offers a solution. The inspiration behind this project came from a friend who grew weary of sharing Goodreads exports with me.

I use the data gathered by this scraper in conjunction with another repository to predict book ratings, providing my friends with more personalized book recommendations. Why spend time on books that won't captivate you? Say goodbye to post-book hangovers and dive into another fantastic read instead!

## Usage

1. Install the required dependencies:
pip install requests pandas beautifulsoup4

Set up your Goodreads user ID in the config_sample.py file and rename to config.py
The userID currently being in the file belongs to a fantastic author, Drew Hayes, you should check him out!

Run the script:
python main.py

## Functionality
The script fetches book information such as book ID, title, author, average rating, and user rating. It paginates through the user's bookshelf (to-read and read) to collect comprehensive data.

## License
This project is licensed under the MIT License - see the LICENSE file for details.