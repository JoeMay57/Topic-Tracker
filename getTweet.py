import tweepy as tw
import os
import keyFile

def tweetPull(terms: list, inclusive:bool, noRT:bool, textOnly:bool, overWrite:bool):
    if not keyFile.fileCheck():
        return 

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
        print(len(os.environ.get('Consumer_Key')))
        auth = tw.OAuthHandler(os.environ.get('Consumer_Key'), os.environ.get('Consumer_Secret'))
        auth.set_access_token(os.environ.get('Access_Token'), os.environ.get('Access_Token_Secret'))
    except:
        print('KEY ERROR\n*************\nPlease run setupt \'-s\' or \'--setup\'')
        return 

    api = tw.API(auth, wait_on_rate_limit=True)
    tweets = tw.Cursor(api.search_tweets, q=search_words, result_type= 'mixed', lang= 'en', include_entities= True, count=100).items(100)
    
    from pymongo import MongoClient
    MongoURL = os.environ.get('MongoURL')
    class Connect(object):
        @staticmethod    
        def get_connection():
            return MongoClient(MongoURL)

    client = Connect.get_connection()
    db = client.tweets
    if overWrite:
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
    return