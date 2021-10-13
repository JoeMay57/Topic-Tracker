from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from os import environ as env

def connectionTest(mongoURL=env.get('MongoURL')) -> bool:
    #test connection
    client = MongoClient(mongoURL)
    try:
        client.tweets.command('ping')
    except ConnectionFailure:
        print("SEVER CONNECTION ERROR\n******************\nPlease run setupt \'-s\' or \'--setup\'")
        return False
    return True

def clearDB(mongoURL=env.get('MongoURL')):
    client = MongoClient(mongoURL)
    db = client.tweets
    db.TopicTrack.drop()

def uploadTweets(tweetOBJ, mongoURL=env.get('MongoURL')):
    #upload
   
    client = MongoClient(mongoURL)
    db = client.tweets
    for tweet in tweetOBJ:

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