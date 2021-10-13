#091421 
#version 0.90

import argparse
import sys
from os import environ as env

import keyFile as KF
import MongoConnect as MC
from getTweet import tweetPull

def optionAsk(options:list, question:str = 'Please select one:') -> int:
    print(question)
    for i in range(len(options)):
        print(str(i+1) + '. ' + options[i])
    
    response = None

    while response != 'exit' and response not in range(len(options)+1)[1:]:
        if response != None:
            print("*\nIncorrect entry\nTry again\n*")
        response=input('Enter corresponding number: ')
    
    if response == 'exit':
        sys.exit()
    else:
        return int(response)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pull and analyize recent trends on twitter of the last week', prefix_chars='-+')
    parser.add_argument('--setup','-s', action='store_true', help='Enter Twitter API keys and MongoDB URL')
    parser.add_argument('--pull', '-p', nargs='*', metavar='TOPIC', type=str, help='Search Twitter for tweets containing one or more keywords or hashtags')
    parser.add_argument('-n', '--ntweets', nargs=1, metavar='N', type = int, default=100, help= 'Number of tweets to pull (default is 100)')
    parser.add_argument('--analyze', '-a', action='store_true', help= 'Run analysis generation wizard')
    parser.add_argument('+nr', '++noretweets', action='store_true', help= 'Omit retweets from search results')
    parser.add_argument('+to', '++textonly', action='store_true', help='Omit tweets with media from search results')
    parser.add_argument('+ow', '++overwrite', action='store_true', help= 'Overwrite existing data')
    parser.add_argument('+&', '++inclusive', action='store_true', help= 'Inclusive topic search')


    args = parser.parse_args()



    if args.setup:
        #enter/update keys/secrets and mogo url to be saved
        print('Please enter Twitter API keys and MongoDB URL\n*******************')
        KF.keyUpdate(['Consumer_Key', 'Consumer_Secret', 'Access_Token', 'Access_Token_Secret', 'MongoURL'])

    if args.pull != None or args.analyze:
        if not KF.loadKeys() or not MC.connectionTest():
            sys.exit()


    if args.pull != None:
        tweets = tweetPull(args.pull, args.inclusive, args.noretweets, args.textonly, args.overwrite, args.ntweets)
        if tweets == 404:
            sys.exit()
        elif tweets == None:
            print('Search returned nothing please try again\n*********************')
        else:
            MC.uploadTweets(tweets)  

    if args.analyze:
        print('tbd')
        # print('','***********************************',
        #     'Welcome to analysis wizard!', 'type \'exit\' at any time to exit',
        #     '***********************************', sep='\n')