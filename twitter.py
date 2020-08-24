import MeCab
from requests_oauthlib import OAuth1Session
import requests
import json
import os
import math
import time

class Twitter:

    CK = os.environ.get('CONSUMER_KEY')
    CS = os.environ.get('CONSUMER_SECRET')
    AK = os.environ.get('ACCESS_KEY')
    AS = os.environ.get('ACCESS_SECRET')

    GETURL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    POSTURL = 'https://api.twitter.com/1.1/statuses/update.json'

    def __init__(self):
        """Initialize its own setup"""
        self._authenticate()

    def _authenticate(self, CK=CK, CS=CS, AK=AK, AS=AS):
        """Authorize your account by some keys"""
        try:
            self.tw = OAuth1Session(CK, CS, AK, AS)
            return True
        except:
            return False

    def fecth_tweets(self, max_tweets=20, max_id=None, wait=False, GETURL=GETURL):
        """
        This can get tweets.
        If you would like to gather lots of tweets and create huge corpus,
        you must set wait to True; default value is False.
        Setting wait to True, this can wait while API limit status is limited.
        """
        try:
            tweets = []
            n_iter = math.ceil(float(max_tweets/200))
            print('iter', n_iter)
            max_id = max_id
            for i in range(n_iter):
                print(max_id)
                if i is n_iter-1:
                    params = {
                        'count': max_tweets % 200,
                        'exclude_replies': True,
                        'include_rts': False,
                        'max_id': max_id
                    }
                else:
                    params = {
                        'count': 200,
                        'exclude_replies': True,
                        'include_rts': False,
                        'max_id': max_id
                    }
            
                res = self.tw.get(GETURL, params=params)
                if res.status_code == 200:
                    raw = json.loads(res.text)
                    tweets += [tweet_data['text'] for tweet_data in raw]
                    max_id = raw[-1]['id']
                else:
                    if wait:
                        while (res.status_code != 200):
                            time.sleep(300)
                            res = self.tw.get(GETURL, params=params)
                        raw = json.loads(res.text)
                        tweets += [tweet_data['text'] for tweet_data in raw]
                        max_id = raw[-1]['id']
                    else:
                        break

            return tweets
        except Exception as e:
            print(e)
            return False

    def update_tweet(self, text: str, POSTURL=POSTURL):
        """This can tweet without the case when text length is over 140 letters"""
        try:
            if len(text) > 140:
                print('このテキストは140字以上です。ツイートできません。')
                return False
            else:
                params = {
                    'status': text, 
                }
                result = self.tw.post(POSTURL, params)
                return True

        except Exception as e:
            print(e)
            return False
                