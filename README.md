# Topic-Tracker
### Find and analize data from recent tweets

## Usage:
    >python TopicTracker.py [-h] [--setup] [--pull [TOPIC ...]] [-n N] [--analyze] [+nr] [+to] [+ow] [+&]


## Optional Arguments:
--------------------------

###  > Intial Setup
    --setup, -s           Enter Twitter API keys and MongoDB URL 

Enter API keys/secrets and a MongoDB connection URL to be saved in an .env file

### > Pull Tweets
     --pull [TOPIC ...], -p [TOPIC ...]
                        Search Twitter for tweets containing one or more keywords or hashtags

Pulls 100 tweets containing search terms or hashtags from the past 7 days. 

To pull more than 100 tweets use the following argument:

     -n N, --ntweets N     Number of tweets to pull (default is 100)

>**NOTE**: check the plan tied to the twitter api connection, you may be limited in the rate at which you can pull tweets.
>>For free users that rate is 450 tweets every 15 minutes.

Search/storage mechanics can be altered by including the following tags:

    +nr, ++noretweets     Omit retweets from search results
    +to, ++textonly       Omit tweets with media from search results
    +ow, ++overwrite      Overwrite existing data
    +&, ++inclusive       Inclusive topic search

### > Analyze

    --analyze, -a         Run analysis generation wizard

*TBD*

### > Help   

    -h, --help            show this help message and exit 