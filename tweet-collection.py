import requests
import os
import sqlite3
from datetime import datetime

# Twitter API v2 credentials
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFJNtQEAAAAAHw%2BllzN21%2FpPBfpfSg9ECt7rAjk%3DnI60zQqMzS7pfL0Z3HR8y6h1JfQEHTjXQPFnEkp5sIsLRCxG13"

# SQLite database connection
conn = sqlite3.connect('tesla_tweets.db')
c = conn.cursor()

# Create table to store tweets if not exists
c.execute('''CREATE TABLE IF NOT EXISTS tweets 
             (id_str TEXT PRIMARY KEY, created_at TEXT, text TEXT)''')

# Define function to save tweets to database
def save_tweets_to_db(tweets):
    for tweet in tweets:
        tweet_data = (tweet['id'], tweet['created_at'], tweet['text'])
        c.execute("INSERT OR IGNORE INTO tweets VALUES (?, ?, ?)", tweet_data)
    conn.commit()

# Define function to get tweets using Twitter API v2
def get_tweets(query):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&tweet.fields=created_at,text"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Failed to fetch tweets: {response.status_code}")
        return []

# Search for tweets about Tesla
search_query = "Tesla"
tweets = get_tweets(search_query)

# Save tweets to database
save_tweets_to_db(tweets)

# Close database connection
conn.close()