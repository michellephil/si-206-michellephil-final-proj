from bs4 import BeautifulSoup
import json
import requests
import sqlite3
import csv
import json
import sys
from secrets import *
import tweepy

DBNAME = 'cheerios.db'
def init_db():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error in e:
        print(e)
#Drop Tables
    statement = '''
        DROP TABLE IF EXISTS 'Products';
    '''
    cur.execute(statement)
    conn.commit()

    statement2 = '''
        CREATE TABLE 'Products' (
            'ProductId' INTEGER PRIMARY KEY,
            'ProductName' TEXT NOT NULL,
            'ProductDesc' TEXT NOT NULL,
            'Calories' TEXT NOT NULL,
            'Picture' TEXT NOT NULL
        );
    '''

    cur.execute(statement2)
    conn.commit()

    statement3 = '''
        DROP TABLE IF EXISTS 'Tweets';
    '''
    cur.execute(statement3)
    conn.commit()

    statement4 = '''
        CREATE TABLE 'Tweets' (
        'TweetId' INTEGER PRIMARY KEY AUTOINCREMENT,
        'TweetText' TEXT NOT NULL,
        'RetweetCount' INTEGER,
        'UserId' TEXT NOT NULL,
        'ScreenName' TEXT NOT NULL,
        'Location' TEXT,
        'FollowerCount' INTEGER,
        'ProductId' INTEGER
        );
    '''
    cur.execute(statement4)
    conn.commit()

def insert_data():
    products = get_product_data()
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    tweet_num = 0
    for prod in products:
        ins = (None, prod.product_name, prod.product_description, prod.product_calories_and_wg, prod.product_pic)
        s = 'INSERT OR IGNORE INTO "Products" '
        s += 'VALUES (?, ?, ?, ?, ?)'
        cur.execute(s, ins)
        conn.commit()
        tweet_num += 1
    conn.close()

def insert_tweet_data(tweets):
    products = get_product_data()
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for tweet in tweets:
        for prod in products:
            ins = (tweet.id, tweet.text.encode('utf8'), tweet.retweet_count, tweet.user.id, tweet.user.screen_name, tweet.user.location, tweet.user.followers_count, prod.id_)
            s = 'INSERT OR IGNORE INTO Tweets '
            s += 'VALUES (?,?,?,?,?,?,?,?)'
            cur.execute(s, ins)
            conn.commit()
            # if prod.product_name in tweet.text:
            #     i = prod.id_
            #     s = 'INSERT OR IGNORE INTO Tweets'
            #     s += 'VALUES ?'
            #     cur.execute(s, i)
            #     conn.commit()
    conn.close()

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def get_unique_key(url):
    return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        # print("Making a request for new data...")
        print(url)
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

class Products:
    def __init__(self, product_name, product_description, product_calories_and_wg, product_pic, id):
        self.product_name = product_name
        self.product_description = product_description
        self.product_calories_and_wg = product_calories_and_wg
        self.product_pic = product_pic
        self.id_ = id
        return

    def __str__(self):
        return '{}: {} ({})'.format(self.product_name, self.product_description, self.product_calories_and_wg)

def get_product_data():
    baseurl = 'https://www.cheerios.com'
    catalog_url = baseurl + '/products'
    list_products = []
    page_text = make_request_using_cache(catalog_url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    page_content = page_soup.find_all('div', class_ = 'mod-product')
    for product in page_content:
        product_name = product.find('span', class_ = 'title-product').text
        product_description = product.find('p', class_ = 'description-product').text
        product_calories_and_wg = product.find('div', class_ = 'content-c-w').text.strip()
        product_pic = baseurl + product.find('img')['src']
        # link = product.find('a')['href']
        # sproduct_page = baseurl + link
        # sp_text = make_request_using_cache(sproduct_page)
        # sp_soup = BeautifulSoup(sp_text, 'html.parser')
        # sp_content = sp_soup.find_all('div', id = 'ProductModule')
        # for s_prod in sp_content:
        #     benefits = s_prod.find_all('li', class_ = 'check')
        #
        # print(benefits)
        ins = Products(product_name = product_name, product_description = product_description, product_calories_and_wg = product_calories_and_wg, product_pic = product_pic, id = 0)
        list_products.append(ins)
    # for product in list_products:
    #     print(product)
    return list_products

def get_tweets(search_term):
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=search_term).items(100)]
    return searched_tweets

if __name__ == '__main__':
    get_product_data()
    init_db()
    insert_data()
    search_term = 'Cheerios' #ASK MATT ABOUT THIS
    tweets = get_tweets(search_term)
    insert_tweet_data(tweets)
