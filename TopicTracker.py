#091421 
#version 0.85

import keyFile
import getTweet
import argparse


if __name__ == "__main__":
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
        keyLocations = ['Consumer_Key', 'Consumer_Secret', 'Access_Token', 'Access_Token_Secret', 'MongoURL']
        keyFile.keyUpdate(keyLocations)


    if args.pull != None:
        keyFile.loadKeys()
        getTweet.tweetPull(args.pull, args.inclusive, args.noretweets, args.textonly, args.overwrite)

    if args.analyze:
        print('tbd')