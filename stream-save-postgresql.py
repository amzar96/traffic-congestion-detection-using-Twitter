import requests
from datetime import datetime, timedelta
from unidecode import unidecode
import re
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import json
from geopy.geocoders import Nominatim
import malaya
from fuzzywuzzy import fuzz
import sqlite3
import function as fp 

sqlite_file = './tweetdata.db'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

consumer_key = 'YDQTpRIw3Eu3QWZjm7i1I2TjA'
consumer_secret = 'ifUyV84GKZHbnVBsWWqBdKUs7NAOwHF81tBjpntu27gI358VOL'
access_token = '75163309-r39wFPr8ozJohjbgxrcaCMEtk7jqXZB9nSm9mGSKN'
access_token_secret = 'iUHaw9HQSOwhrZ9YBevADvh4V2ZlcNfT3KzzCATA6QeUZ'

class StdOutListener(StreamListener):
    def on_data(self, data):
        try:
            print(data)
            fp.run_this(data)
            return True

        except Exception as e:
            print(e)

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    while True:
        try:
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            stream = Stream(auth, l)
            stream.filter(
                locations = [101.418145, 2.756636, 101.736528, 3.277724]
            )
        except Exception as e:
            print('outer exception:', e)
            time.sleep(60)
            continue
