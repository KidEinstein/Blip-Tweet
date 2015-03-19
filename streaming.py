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
# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="NJCjifiHUVAJZy7YWAzh7oTtt"
consumer_secret="BIU0bilnYQpB7i0wZB4ziQHeGBr5pk2xf7Mb4hjJ3P6sNdFWi7"
# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="601757547-6AHTD2XJVLoir2HfRp2yvwrPREtQy3O60dre03h1"
access_token_secret="AvBXrocbNYEAKLcvalyT6OoblkFvMiAInnZ1MePuGpoEX"
tweets = list()
h = HTMLParser.HTMLParser()
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
        if len(tweets) >= 5:
            output_text = ''
            output_file = open('output.txt', 'w')
            i = 5
            while i > 0 and len(tweets) > 0:
                item = tweets.pop()
                tweet = json.loads(item)
                screen_name = '@' + tweet['user']['screen_name'] + " : "
                tweet_text = tweet['text']
                tweet_text = tweet_text.encode('ascii', 'ignore')
                if tweet_text == '' or re.search(r'^RT|^\n', tweet_text): 
                    continue
                tweet_text = tweet_text.replace('\n', ' ').replace('\r', '')
                tweet_text = re.sub('https?:\/\/[^\s]*', '', tweet_text)
                tweet_text = re.sub(' +', ' ', tweet_text)  
                tweet_text = h.unescape(tweet_text)
                print(screen_name)
                print(tweet_text)
                output_text += screen_name + tweet_text + " "
                i -= 1
            fcntl.flock(output_file.fileno(), fcntl.LOCK_EX)
            output_file.write(output_text)
            output_file.close()           
        if len(tweets) > 50:
            tweets = []
        time.sleep(5)
if __name__ == '__main__':
    worker = Thread(target = parse_tweet)
    worker.start()
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['basketball'])
    
