from __future__ import absolute_import, print_function
from Queue import Queue
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from threading import Thread
import time
import json
import fcntl
import re
import HTMLParser
from collections import deque
import requests
from auth2 import *

tweets = list()
output_text = deque()
h = HTMLParser.HTMLParser()
search_term = 'hello'

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        tweets.append(data)
        return True
    
    def on_error(self, status):
        print(status)


def check_tag():
    global stream
    global search_term
    global tweets
    print(search_term)
    try:
        fetched_data = requests.get('http://results.zz.mu/hashtag.txt')
    except:
        return;
    print(fetched_data.text)
    print(fetched_data.text)
    if not stream.running:
        time.sleep(5)
        stream.filter(track=[search_term], async=True)
    if fetched_data.text != search_term:
        print('Killed it!')
        search_term = fetched_data.text
        tweets = []
        if stream.running:
            stream.disconnect()
            time.sleep(5)
            stream.filter(track=[search_term], async=True)
            time.sleep(5)
    


def parse_tweet():
    global tweets
    while True:
        try:
            check_tag();
            output_file = open('output.txt', 'w')
            while tweets:
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
            time.sleep(1)
        except:
            pass

        
if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=[search_term], async=True)
    worker = Thread(target = parse_tweet)
    worker.start()

