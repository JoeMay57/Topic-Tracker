from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from os import environ as env
import re

def connectionTest(mongoURL=env.get('MongoURL')) -> bool:
    #test connection
    try:
        MongoClient(mongoURL).tweets.command('ping')
    except ConnectionFailure:
        print("SEVER CONNECTION ERROR\n******************\nPlease run setupt \'-s\' or \'--setup\'")
        return False
    return True

def clearDB(mongoURL=env.get('MongoURL')):
    MongoClient(mongoURL).tweets.TopicTrack.drop()

def uploadTweets(tweetOBJ, mongoURL=env.get('MongoURL')):
    #upload
   
    db = MongoClient(mongoURL).tweets.TopicTrack
    for tweet in tweetOBJ:

        db.insert_one(
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

def searchTweets(search_term:str, yAx:str, xAx:str, mongoURL=env.get('MongoURL') ):
    #query tweets matching search term and one other corresponding axis
    x = []
    y = []

    client = MongoClient(mongoURL)
    db = client.tweets.TopicTrack
    if search_term == '':
        result = db.find()
    else:
        result = db.find({yAx: re.compile(search_term, re.IGNORECASE)})

    if result == None:
        print("No Data points found\n******************\nPlease try again")
        return None, None
    else:
        for entry in result:
            y.append(entry[yAx])
            x.append(entry[xAx])
        return x, y
        