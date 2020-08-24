import MeCab
from requests_oauthlib import OAuth1Session
import requests
import json
import os

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
        try:
            self.tw = OAuth1Session(CK, CS, AK, AS)
            return True
        except:
            return False

    def fecth_tweets(self, max_tweets=20, GETURL=GETURL):
        try:
            if max_tweets > 200:
                max_tweets = 200
            elif max_tweets <= 0:
                max_tweets = 1
            else:
                max_tweets = int(max_tweets)
            params = {
                'count': max_tweets,
                'exclude_replies': True,
                'include_rts': False,
            }
            res = self.tw.get(GETURL, params=params)
            raw = json.loads(res.text)
            tweets = [tweet_data['text'] for tweet_data in raw]
            return tweets
        except Exception as e:
            print(e)
            return False

    def update_tweet(self, text: str, POSTURL=POSTURL):
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
                