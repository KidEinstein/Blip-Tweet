from __future__ import absolute_import, print_function
from Queue import Queue
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from threading import Thread
import tweepy
import time
import json
import fcntl
import re
import HTMLParser
from collections import deque
SEARCH_TERM = '#CWC15'
# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="NJCjifiHUVAJZy7YWAzh7oTtt"
consumer_secret="BIU0bilnYQpB7i0wZB4ziQHeGBr5pk2xf7Mb4hjJ3P6sNdFWi7"
# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="601757547-6AHTD2XJVLoir2HfRp2yvwrPREtQy3O60dre03h1"
access_token_secret="AvBXrocbNYEAKLcvalyT6OoblkFvMiAInnZ1MePuGpoEX"
tweets = list()
output_text = deque()
h = HTMLParser.HTMLParser()
output_file = open('output.txt', 'w')
class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        tweets.append(data)
        return True
    def on_error(self, status):
        print(status)
def parse_tweet():
    global tweets
    while True:
        output_file = open('output.txt', 'w')
        i = 5
        for i in range(len(tweets)):
            item = tweets.pop()
            tweet = json.loads(item)
            tweet_text = tweet['text']
            if tweet_text == '' or re.search(r'^RT|^\n', tweet_text):
                continue
            screen_name = '@' + tweet['user']['screen_name'] + " : "
            tweet_text = tweet_text.encode('ascii', 'ignore')
            tweet_text = tweet_text.replace('\n', ' ').replace('\r', '')
            tweet_text = re.sub('https?:\/\/[^\s]*', '', tweet_text)
            tweet_text = re.sub(' +', ' ', tweet_text)  
            tweet_text = h.unescape(tweet_text)
            print(screen_name)
            print(tweet_text)
            output_text.append(screen_name + tweet_text + " ")
            if len(output_text) > 5:
                output_text.popleft()
        fcntl.flock(output_file.fileno(), fcntl.LOCK_EX)
        output_file.writelines(output_text)
        output_file.close()           
        if len(tweets) > 50:
            del tweets[:-10]
        time.sleep(5)
if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
##    api = tweepy.API(auth)
##    max_tweets = 10
##    searched_tweets = [status for status in tweepy.Cursor(api.search, q=SEARCH_TERM).items(max_tweets)]
##    for tweet in searched_tweets:
##        tweet_text = tweet.text
##        if tweet_text == '' or re.search(r'^RT|^\n', tweet_text):
##            continue
##        screen_name = '@' + tweet.user.screen_name + " : "
##        tweet_text = tweet_text.encode('ascii', 'ignore')
##        tweet_text = tweet_text.replace('\n', ' ').replace('\r', '')
##        tweet_text = re.sub('https?:\/\/[^\s]*', '', tweet_text)
##        tweet_text = re.sub(' +', ' ', tweet_text)  
##        tweet_text = h.unescape(tweet_text)
##        print(screen_name)
##        print(tweet_text)
##        output_text.append(screen_name + tweet_text + " ")
##        if len(output_text) > 5:
##            output_text.popleft()
##    fcntl.flock(output_file.fileno(), fcntl.LOCK_EX)
##    output_file.writelines(output_text)
##    output_file.close()           
##    if len(tweets) > 50:
##        del tweets[:-10]
##    time.sleep(5)
        
    worker = Thread(target = parse_tweet)
    worker.start()
    stream = Stream(auth, l)
    stream.filter(track=[SEARCH_TERM])
    
