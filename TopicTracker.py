#091421 
#version 1.2

from json.decoder import JSONDecodeError
from os.path import exists as file_exists
import sys
import json
from datetime import datetime





def keyUpdate(locs: list, values: list): #funciton for saving data to json
    if file_exists('keys.json'): #if file exists load existing data
        with open ('keys.json', 'r') as f:
            data = json.load(f)
    else:
        data = {}

    while len(locs) > len(values): #locations without data will be cleared, data without location will be ignored
            values.append('')
 
    for l in range(len(locs)): #update values
        data[locs[l]] = values[l]

    with open('keys.json', 'w+') as file:
            json.dump(data, file)

#check input for shared issues
args = sys.argv[1:]
if len(args) == 0:
    args = ['help', ' ']

if args[0] not in ['pull', 'analysis', 'setDB', 'setKeys', 'help']:
    print('UNRECOGNIZED COMMAND\n')
    sys.exit()

if len(args) < 2:
    print('ARGUMENT ERROR\n')
    sys.exit()

mods = [] #remove -mods from arguments
#print(args)
for i in args:
    if type(i) is str:
        if i[0] == '-':
            mods.append(i)
for i in mods:
    args.remove(i)

if 'help' in args or '-h' in mods:
    print('Usage:\n  python TopicTracker.py <comand> [options] -x -y\n',
            'Comands:',
            ' pull    \tpull tweets [n tweets] [end date XXXX-XX-XX] [search term 1] [search term 2] ...',
            '\t-nr \tNo retweets',
            '\t-to \tText Only',
            '\t-and\tInclusive topic searching',
            '\t-ow \tOverwrite existing data',
            ' analysis\tview analysis figures',
            ' setDB   \tset MongoDB URL [URL]',
            ' setKeys \tset Twitter API keys [Consumer Key] [Consumer Secret] [Access Token] [Access Token Secret]',
            ' help    \tshow help',
            sep ='\n')
    sys.exit()

if args[0] == 'setKeys':
    n = 0
    if len(args) >= 5 and all(type(x) is str for x in args[1:5]):
        keyUpdate(['Consumer Key', 'Consumer Secret', 'Access Token', 'Access Token Secret'], args[1:])
    else:
        print('ARGUMENT ERROR\n')
    sys.exit()

elif args[0] == 'setDB':
    if len(args) >= 2 and type(args[1]) is str: #argument validation
        keyUpdate(['MongoURL'], [args[1]]) 
    else: 
        print('ARGUMENT ERROR\n')
    sys.exit()

elif args[0] == 'pull':
   
    if len(args) < 3 or any(type(x) is not str for x in args [2:]) or int(args[1]) <= 0: #argument validation
        print('ARGUMENT ERROR\n')
        sys.exit()
    try: 
        test = datetime.strptime(args[2], '%Y-%m-%d')
        date_until = args[2]
    except ValueError:
        print('INCORRECT DATE ENTRY\n')
        sys.exit()
    

    import tweepy as tw

    if '-and' in mods:
        x = ' '
    else:
        x = ' OR '
    search_words = '(' + args[3]

    for w in args[4:]:
        search_words = search_words + x + w
    
    search_words = search_words + ')'

    if '-nr' in mods:
        search_words = search_words + ' -is:retweet -"RT"'
    
    if '-to' in mods:
        search_words = search_words + ' -has:media'
    
    print(search_words)

    with open('keys.json', 'r') as f:
        data = json.load(f)
        auth = tw.OAuthHandler(data['Consumer Key'], data['Consumer Secret'])
        auth.set_access_token(data['Access Token'], data['Access Token Secret'])
        MongoURL = data['MongoURL']

    api = tw.API(auth, wait_on_rate_limit=True)

    print(args)
    tweets = tw.Cursor(api.search, q=search_words, results_type= 'mixed', lang= 'en', include_entities= True, count=100).items(int(args[1]))


    

   #Mongo Connection
    from pymongo import MongoClient
    class Connect(object):
        @staticmethod    
        def get_connection():
            return MongoClient(MongoURL)

    client = Connect.get_connection()
    db = client.tweets
    if '-ow' in mods:
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
