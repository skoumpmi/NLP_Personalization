# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:38:44 2020

@author: mtsourma
"""
import configparser
import time
import datetime
import csv
import pandas as pd
#from twython import Twython
import tweepy
import os

now = datetime.datetime.now()
day = int(now.day)
month = int(now.month)
year = int(now.year)

config = configparser.ConfigParser()
config.read('configuration.ini')

CONSUMER_KEY = config['AuthenticationParams']['consumer_key']
CONSUMER_SECRET = config['AuthenticationParams']['consumer_secret']
OAUTH_TOKEN = config['AuthenticationParams']['oauth_token']
OAUTH_TOKEN_SECRET = config['AuthenticationParams']['oauth_token_secret']


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)

# Get twitter ids and with a condition to avoid limitation errors
userIds = []
tweetIds = []
tweetCreated_at = []
screen_name = []
tweets_counter = 0

filePath = '.\\SampleData\\'

inputFilePath = os.path.join(filePath, "twitterIds_dataset_famous.csv")
f = open(inputFilePath)
data = csv.reader(f, delimiter=',')
data = [row for row in data]
f.close()
# Create a data frame
df = pd.DataFrame(data)
df = pd.DataFrame(data, columns=['userId', 'screen_name', 'tweetId', 'created_at'])

counter = 0
idlist = df["userId"].tolist()

#Get the tweets of every user
with open(filePath + 'samsung_dataset_without_retweets.csv', 'wt') as nf:
    nf.write('userId,tweetId,tweet\n')
    for k in range(0, len(df['userId'])):
        w = csv.writer(nf, delimiter=',', lineterminator='\n') 
        counter = k    
        try:
            tweets = tweepy.Cursor(api.user_timeline, user_id=df['userId'][k], tweet_mode="extended", count=3000, since_id=None, max_id=None, exclude_replies=True).items()
            for tweet in tweets:
                # print('%s' % (tweet.full_text.encode('UTF-8')))
                if df['userId'][k] == str(tweet.user.id):
                    if hasattr(tweet, 'retweeted_status') == False:                            
                        if hasattr(tweet, 'full_text') == False:
                            print('%s,%s' % (tweet.id, tweet.full_text.encode('UTF-8')))   
                            row = [df['userId'][k], tweet.id, tweet.full_text.encode('UTF-8')]   
                            w.writerow(row)                            
                        else:
                            print('%s,%s' % (tweet.id, tweet.full_text.encode('UTF-8')))   
                            row = [df['userId'][k], tweet.id, tweet.full_text.encode('UTF-8')]   
                            w.writerow(row)
                    else:
                        if tweet.is_quote_status == True:
                            if tweet.full_text.startswith("RT @" + df['screen_name'][k] + ":"):
                                print('%s,%s' % (tweet.id, tweet.full_text.encode('UTF-8')))   
                                row = [df['userId'][k], tweet.id, tweet.full_text.encode('UTF-8')]   
                                w.writerow(row)   
            if counter == len(df['screen_name']):
                break
        except tweepy.TweepError:
            time.sleep(60*15)
            print(k)
            continue
        except StopIteration:
            break
nf.close() 
   