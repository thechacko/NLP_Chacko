import requests
import json
from bs4 import BeautifulSoup as bs
from loguru import logger
import time
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import psycopg2
from sql_queries import CREATE_TABLE, CHECK_TABLE, INSERT_INTO_TABLE, DATA_CHECK
import configparser


# importing configs
try:
    config = configparser.ConfigParser()
    config.read('dbconfig.ini')
    dbconfigs={
        'host': config['PostgreSQL']['host'],
        'database': config['PostgreSQL']['database'],
        'user': config['PostgreSQL']['user'],
        'password': config['PostgreSQL']['password'],
        'port': config['PostgreSQL']['port']
    }
    logger.info("Credentials fetched")
except Exception as e:
    logger.error(f"Unable to fetch credentials: {e}")

DATABASE = dbconfigs['database']
SCHEMA = 'rss_feeds'
TABLE = 'livemint'
DATE = datetime.today().strftime("%Y-%m-%d")

# Scraping
try:
    url = 'https://www.livemint.com/sitemap/yesterday.xml'
    r = requests.get(url)
    with open(f'./raw/livemint_{DATE}.txt', 'wb') as f:
        f.write(r.content)
except Exception as e:
    logger.error(f"Unable to scrape data: {e}")

try:
    with open(f'./raw/livemint_{DATE}.txt', 'rb') as f:
        loaded_content = f.read()
    
    loaded_soup = bs(loaded_content, features='xml')
    
    urls = loaded_soup.find_all('url')

    yday_news = []

    for u in urls:
        art_data = {}
        art_data['news_link'] = u.find('xhtml:link')['href']
        art_data['pub_date'] = u.find('news:publication_date').text
        art_data['title'] = u.find('news:title').text
        art_data['keywords'] = u.find('news:keywords').text
        yday_news.append(art_data)

    df = pd.json_normalize(yday_news)

    df.insert(2, 'category', df['news_link'].apply(lambda x: x.split("/")[3]))
    df = df[df['category']=='companies']
    df.drop('category', axis=1, inplace=True)

    article_text = []
    for link in tqdm(df['news_link']):
        time.sleep(1)
        r = requests.get(link)
        soup = bs(r.text, 'html.parser')
        article_text.append(" ".join([item.text for item in soup.find_all('p')]))

    df['articles'] = article_text
    df['scraped_date'] = DATE
    logger.info("Scraping succesfully completed")
except Exception as e:
    logger.error(f"Unable to scrape data: {e}")

# Saving scraped data
try:
    filename = f'./data/livemint_{DATE}.json'
    df.to_json(filename, orient='records', lines=True)
    logger.info(f"Saved data to {filename}")
except Exception as e:
    logger.error(f"Unable to save data: {e}")

# Reloading json to check
try:
    with open(f'./data/livemint_{DATE}.json', 'r') as f:
        livemint_data = [json.loads(line) for line in f.readlines()]
    logger.info("Reloaded saved scraped data")
except Exception as e:
    logger.error(f"Unable to reload saved data: {e}")

# Storing scraped data to database
try:
    with psycopg2.connect(**dbconfigs) as conn:
        logger.info("Able to connect with database")
except Exception as e:
    logger.info(f"Unable to connect with database: {e}")

try:
    with psycopg2.connect(**dbconfigs) as conn:
        with conn.cursor() as cur:
            check_table = CHECK_TABLE.format(SCHEMA, TABLE)
            cur.execute(check_table)
            if bool(cur.fetchone()[0]):
                logger.info(f"Table '{TABLE}' exists. Moving On")
                conn.commit()
            else:
                logger.info(f"Table does not exist. Creating table: '{TABLE}'")
                cur.execute(CREATE_TABLE)
                conn.commit()
                logger.info(f"Table '{TABLE}' created")
except Exception as e:
    logger.error(f"Unable to connect to table: {e}")

try:
    with psycopg2.connect(**dbconfigs) as conn:
        with conn.cursor() as cur:
            cur.execute(INSERT_INTO_TABLE, (DATE, json.dumps(livemint_data)))
            conn.commit()
    logger.info("Data insertion successful")
except Exception as e:
    logger.error("Unable to insert data: {e}")

# Testing if data stored
try:
    with psycopg2.connect(**dbconfigs) as conn:
        with conn.cursor() as cur:
            cur.execute(DATA_CHECK.format(DATE))
            todays_date = cur.fetchone()[1]
            logger.info(f"Today's date: {todays_date}")
            conn.commit()
except Exception as e:
    logger.error(f"Unable to fetch data: {e}")
