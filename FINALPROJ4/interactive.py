from flask import Flask, render_template
import requests
from proj4_cherrios import *
import sqlite3

DBNAME = 'cheerios.db'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/flavors')
def flavors():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    s = 'SELECT ProductName, Picture '
    s += 'FROM Products '
    cur.execute(s)
    info = []
    for row in cur:
        info.append(row)
    return render_template('flavors.html', info=info)

@app.route('/descriptionsandcalories')
def search():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    s = 'SELECT ProductName, Picture, ProductDesc, Calories '
    s += 'FROM Products '
    cur.execute(s)
    cals = []
    for row in cur:
        cals.append(row)
    return render_template('desc.html', cals=cals)

@app.route('/tweets')
def tweets():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    s = 'SELECT TweetText, ScreenName, Location '
    s += 'FROM Tweets '
    cur.execute(s)
    tweet = []
    for row in cur:
        tweet.append(row)
    return render_template('twitter.html', tweet=tweet)

if __name__ == '__main__':
    app.run(debug=True)
