# Import dependencies
#import json
import os
import tweepy
import csv
import time
import re
from scraper import Scrape

# Declare constant variables
API_KEY = os.environ['API_KEY']
API_KEY_SECRET = os.environ['API_KEY_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
BOT_USER = 'StockrAI'
WAIT_TIME = 15
LAST_ID = 1344276911304880128
#SECRETS_FILE = 'secrets.json'
#LOG_FILE = 'tweet_log.csv'

# def load_secrets():
#     """
#     Load secret keys from json file
#     """
#     with open(SECRETS_FILE, 'r') as f:
#         secrets = json.load(f)
#     return secrets

def generate_auth():
    """
    Set up authentication using keys
    """
    #secrets = load_secrets()
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth

def create_api(auth):
    """
    Instantiate API object and verify credentials
    """
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("== Authentication successful")
    except Exception as e:  # Print error if authentication unsuccessful
        print(e)
    return api

def send_tweets(api, mentions):
    """
    Publish tweets as responses to mentions
    """
    for mention in reversed(mentions):  # Reverse list to have most recent tweets first
        ticker = scan_tweet(mention['text'])
        if mention['username'] != BOT_USER and ticker != None:
            print(f"""++ New mention @ {mention['timestamp']} {{'id': {mention['id']}, 'username': '{mention['username']}', 'text': '{mention['text']}'}}""")
            body = construct_tweet(mention['username'], ticker) # Construct body of tweet
            api.update_status(body, mention['id'])  # Post tweet
            #log(mention)
            LAST_ID = mention['id']
    return LAST_ID

# def get_last_id():
#     """
#     Retrieve last tweet ID from text file
#     """
#     with open(LOG_FILE, 'r') as f: 
#         data = f.readlines()[-1].split(',')
#         return data[1]

# def log(mention):
#     """
#     Append mentioned tweet data to log csv file
#     """
#     with open(LOG_FILE, 'a', newline='') as f:
#         writer = csv.writer(f)
#         line = [mention['timestamp'],mention['id'],mention['username'],mention['text']]
#         writer.writerow(line)

def scan_tweet(text):
    """
    Search for stock ticker in tweet
    """
    try:
        ticker = re.findall(r'\$([a-zA-Z]{1,4})', text)[0]
        return ticker
    except:
        return None
    
def construct_tweet(username, ticker):
    """
    Create tweet body with necessary data and formatting
    """
    try:
        data = Scrape(ticker)
        body = f"""
@{username}
${ticker.upper()} - {data['date']}
High: {data['high']}
Low: {data['low']}
Open: {data['open']}
Close: {data['close']}
Volume: {data['volume']}
Adjusted Close: {data['adj_close']}
"""
    except:
        body = f"""
@{username}
Sorry, ${ticker.upper()} is not a supported ticker :(
"""
    return body

if __name__ == '__main__':
    auth = generate_auth()
    api = create_api(auth)
    print(f'== Now scanning for tweets mentioning @{BOT_USER}')
    # Constantly scan for new tweets mentioning bot account
    while True:
        mentions = [{'timestamp':mention.created_at,'id':mention.id,'username':mention.user.screen_name,'text':mention.text} for mention in api.mentions_timeline(since_id=LAST_ID)]  # Create list of dictionaries for each mention tweet since last ID
        LAST_ID = send_tweets(api, mentions)  # Post tweet replies and get last ID
        time.sleep(WAIT_TIME)