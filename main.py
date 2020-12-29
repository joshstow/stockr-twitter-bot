# Import dependencies
import json
import tweepy

# Load secret keys from json file
with open('secrets.json') as f:
    secrets = json.load(f)
    print(secrets)

# Set up authentication using keys
auth = tweepy.OAuthHandler(secrets['API_KEY'], secrets['API_KEY_SECRET'])
auth.set_access_token(secrets['ACCESS_TOKEN'], secrets['ACCESS_TOKEN_SECRET'])

# Instantiate API object
api = tweepy.API(auth)

# Create a tweet
api.update_status("Hello World")