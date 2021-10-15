#091421 
#version 1.00 (101421)

import argparse
import sys

import keyFile as KF
import MongoConnect as MC
import topicAnalysis as TA
import getTweet as GT


def optionAsk(options:list, question:str = 'Please select one:') -> int:
    print(question)
    nums = range(len(options) + 1)[1:]
    for i in nums:
        print(str(i) + '. ' + options[i-1])
    
    response = ''

    while response != 'exit':
        if response != '':
            print("*\nIncorrect entry\nTry again\n*")
        response=input('Enter corresponding number: ')

        try:
            if int(response) in nums:
                break
        except ValueError:
                continue
    
    if response == 'exit':
        sys.exit()
    else:
        return options[int(response) - 1]

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
        tweets = GT.tweetPull(GT.queryGen(args.pull, args.inclusive, args.noretweets, args.textonly, args.overwrite), args.ntweets)
        if tweets == 404:
            sys.exit()
        elif tweets == None:
            print('Search returned nothing please try again\n*********************')
        else:
            MC.uploadTweets(tweets)  

    if args.analyze:
        print('','***********************************',
            'Welcome to analysis wizard!', 'type \'exit\' at any time to exit',
            '***********************************', sep='\n')
        gType = optionAsk(['Histogram', 'Scatterplot'], 'What type of graph shall we make?')
        if gType == 'Histogram':
            yAxis = optionAsk(['username', 'text', 'RT', 'Fav'], 'What should be examined?')
            xAxis = 'date'
        else:
            xAxis = optionAsk(['username', 'date', 'text', 'RT', 'Fav'], 'What will be the x axis?')
            yAxis = optionAsk(['username', 'date', 'text', 'RT', 'Fav'], 'What will be the y axis? \n(don\'t choose the same unless you like straight lines)')
        
        searchK = input('Enter topic search keyword for y axis; \nleave blank to use all data:')
        x, y = MC.searchTweets(searchK, yAxis, xAxis)

        if gType == 'Histogram':
            TA.plotHist(x, searchK)
        elif gType == 'Scatterplot':
            TA.plotScatter(x, y, xAxis, yAxis, searchK)
            

        

        

