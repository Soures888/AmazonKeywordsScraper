# Amazon Scraper

# Description

Scraper collects data from Amazon.com search results under a specific Zip code, calculates the item's position and saves it to the database.

# Requirements

- Python3.8 +
- pip3

# Installation

```
git clone -
pip install -u requirements.txt
```

# Running
1. In the res directory, create a *keywords.txt* file
2. In the main directory create a .env file with the settings:
```
REQUEST_TIMEOUT=1
PAGE_PER_KEYWORD=10
PARSING_ZIP_CODE=10001
SAVE_RESPONSE_PAGE=True
```
3. Run a python script
```bash
python main.py
```
4. After a while, the data will begin to appear in the database.db database

# How does it work?

1. After start, the res/keywords.txt file opens and keywords for search are loaded
2. ORM module connects to the database and creates tables
3. The *ParseClient* client is initialized
4. Parsing N pages per keyword
5. After receiving the data about the keyword, the results are saved to the database in the columns: *dt, product_id (Get from product url), keyword, rank_type (organic/sponsored), rank, page_number, bestseller_badge (True/False), amazonchoice_badge (True/False)*

# Saved data example


![](https://imgur.com/KUR427p.png "Saved Data")