#091421 
#version 0.65

from json.decoder import JSONDecodeError

import sys
import json
from datetime import datetime
import argparse
import tweepy as tw

def keyUpdate(locs: list): #funciton for saving data to json
    from os.path import exists as file_exists

    print('Type \'exit\' to exit and leave empty to not update field\n')
    j = 0
    values = []
    while 'exit' not in values and j < len(locs):
        values.append(input(locs[j] + ': '))
        j += 1
        if values[j-1] == '':
            values.pop(j-1)
            locs.pop(j-1)
            j-=1
        
    if 'exit' in values:
        return

    if file_exists('keys.json'): #if file exists load existing data
        with open ('keys.json', 'r') as f:
            data = json.load(f)
    else:
        data = {}

    for l in range(len(locs)): #update values
        data[locs[l]] = values[l]

    with open('keys.json', 'w+') as file:
            json.dump(data, file)
    return

def tweetPull(terms: list, inclusive:bool, noRT:bool, textOnly:bool):
    
    if inclusive:
        x = ' '
    else:
        x = ' OR '
    search_words = '(' + terms[0]

    for w in terms[1:]:
        search_words = search_words + x + w
    
    search_words = search_words + ')'

    if noRT:
        search_words = search_words + ' -is:retweet -"RT"'
    
    if textOnly:
        search_words = search_words + ' -has:media'
    
    try:
        with open('keys.json', 'r') as f:
            data = json.load(f)
            auth = tw.OAuthHandler(data['Consumer Key'], data['Consumer Secret'])
            auth.set_access_token(data['Access Token'], data['Access Token Secret'])
            MongoURL = data['MongoURL']
    except:
        print('KEY ERROR\n*************\nPlease run setupt \'-s\' or \'--setup\'')
        return None,None

    api = tw.API(auth, wait_on_rate_limit=True)
    tweets = tw.Cursor(api.search, q=search_words, results_type= 'mixed', lang= 'en', include_entities= True, count=100).items(450)
    return tweets,MongoURL



parser = argparse.ArgumentParser(description='Pull and analyize recent trends on twitter of the last week', prefix_chars='-+')
parser.add_argument('--setup','-s', action='store_true', help='Enter Twitter API keys and MongoDB URL')
parser.add_argument('--pull', '-p', nargs='*', metavar='TOPIC', type=str, help='Search Twitter for tweets containing one or more keywords or hashtags')
parser.add_argument('--analyze', '-a', action='store_true', help= 'Run analysis generation wizard')
parser.add_argument('+nr', '++noretweets', action='store_true', help= 'Omit retweets from search results')
parser.add_argument('+to', '++textonly', action='store_true', help='Omit tweets with media from search results')
parser.add_argument('+ow', '++overwrite', action='store_true', help= 'Overwrite existing data')
parser.add_argument('+&', '++inclusive', action='store_true', help= 'Inclusive topic search')


args = parser.parse_args()



if args.setup:
    print('Please enter Twitter API keys and MongoDB URL\n*******************')
    keyLocations = ['Consumer Key', 'Consumer Secret', 'Access Token', 'Access Token Secret', 'MongoURL']
    keyUpdate(keyLocations)


if args.pull != None:
    tweets, MongoURL = tweetPull(args.pull, args.inclusive, args.noretweets, args.textonly)
    
   #Mongo Connection
    from pymongo import MongoClient
    class Connect(object):
        @staticmethod    
        def get_connection():
            return MongoClient(MongoURL)

    client = Connect.get_connection()
    db = client.tweets
    if args.overwrite:
        db.TopicTrack.drop()
    #upload
    for tweet in tweets:

        db.TopicTrack.insert_one(
            {"ID": tweet.id,
            "username": tweet.user.screen_name,
            "date": tweet.created_at,
            "text": tweet.text,
            "url": tweet.entities['urls'],
            "hashtags": tweet.entities['hashtags'],
            "geo": tweet.geo,
            "RT": tweet.retweet_count,
            "Fav": tweet.favorite_count}
        )

if args.analyze:
    print('tbd')