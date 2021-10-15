from pymongo.common import SERVER_SELECTION_TIMEOUT
import tweepy as tw
from os import environ as env

def queryGen(terms: list, inclusive:bool, noRT:bool, textOnly:bool, overWrite:bool, numtweet:int=100) -> str:
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
    return search_words

def tweetPull(search_words:str, numtweet:int=100):
    try:
        auth = tw.OAuthHandler(env.get('Consumer_Key'), env.get('Consumer_Secret'))
        auth.set_access_token(env.get('Access_Token'), env.get('Access_Token_Secret'))
    except:
        print('KEY ERROR\n*************\nPlease run setupt \'-s\' or \'--setup\'')
        return 404

    api = tw.API(auth, wait_on_rate_limit=True)
    return tw.Cursor(api.search_tweets, q=search_words, result_type= 'mixed', lang= 'en', include_entities= True, count=100).items(numtweet)