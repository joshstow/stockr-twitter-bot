# Import dependencies
import json
import tweepy
import csv
import time

# Declare constant variables
BOT_USER = 'StockrAI'
WAIT_TIME = 15
SECRETS_FILE = 'secrets.json'
LOG_FILE = 'tweet_log.csv'
ID_FILE = 'last_id.txt'

def load_secrets():
    """
    Load secret keys from json file
    """
    with open(SECRETS_FILE, 'r') as f:
        secrets = json.load(f)
    return secrets

def generate_auth():
    """
    Set up authentication using keys
    """
    secrets = load_secrets()
    auth = tweepy.OAuthHandler(secrets['API_KEY'], secrets['API_KEY_SECRET'])
    auth.set_access_token(secrets['ACCESS_TOKEN'], secrets['ACCESS_TOKEN_SECRET'])
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
        if mention['username'] != BOT_USER:
            print(f"""++ New mention @ {mention['timestamp']} {{'id': {mention['id']}, 'username': '{mention['username']}', 'text': '{mention['text']}'}}""")
            api.update_status(f"""@{mention['username']} This is a response""", mention['id'])  # Post tweet
            log(mention)
    # Do nothing if no new mentions found
    try:
        update_last_id(mention['id'])
    except:
        return

def get_last_id():
    """
    Retrieve last tweet ID from text file
    """
    with open(ID_FILE, 'r') as f:
        return f.read()

def update_last_id(id):
    """
    Overwrite text file with most recent tweet ID
    """
    with open(ID_FILE, 'w') as f:
        f.write(str(id))

def log(mention):
    """
    Append mentioned tweet data to log csv file
    """
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        line = [mention['timestamp'],mention['id'],mention['username'],mention['text']]
        writer.writerow(line)

if __name__ == '__main__':
    auth = generate_auth()
    api = create_api(auth)
    print(f'== Now scanning for tweets mentioning @{BOT_USER}')
    # Constantly scan for new tweets mentioning bot account
    while True:
        mentions = [{'timestamp':mention.created_at,'id':mention.id,'username':mention.user.screen_name,'text':mention.text} for mention in api.mentions_timeline(since_id=get_last_id())]  # Create list of dictionaries for each mention tweet since last ID
        send_tweets(api, mentions)  # Post tweet replies
        time.sleep(WAIT_TIME)