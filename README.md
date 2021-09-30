# Topic-Tracker
Find and analize data from recent tweets

Usage:
python TopicTracker.py <comand> [options] -x -y\
    Comands:
pull        pull tweets [n tweets] [end date XXXX-XX-XX] [search term 1] [search term 2] ...',
    -nr         No retweets
    -to         Text Only
    -and        Inclusive topic searching
    -ow         Overwrite existing data
analysis    view analysis figures
setDB       set MongoDB URL [URL]
setKeys     set Twitter API keys [Consumer Key] [Consumer Secret] [Access Token] [Access Token Secret]
help        show this help