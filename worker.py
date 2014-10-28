# -*- coding: utf-8 -*-
"""
this module controll db insertion
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time
import logging

import pymongo

from tweets import Tweets
from config import *

class Worker(threading.Thread):
    """
    @todo: Intends to use beanstalkd as queue, however beanstalkc didn't
    support py3k yet, use queue instead.
    While using PriorityQueue, user_id may get lost when thread crash.
    """
    def __init__(self, queue):
        self.queue = queue
        self.db = pymongo.MongoClient(env.mongodb_url)["reylgan"]
        super(Worker, self).__init__()

    def _push_to_db(self, data, collect):
        """
        @todo upsert each user info
        """
        logging.info(
            "pushing %d items to collection %s." % (len(data), collect))
        db[collect].insert(data, continue_on_error=True)

    def run(self):
        tweets = Tweets()
        while True:
            user_id = self.queue.get()[-1]
            """
            print (self.name, user_id)
            pull tweet, user's follower & friends
            push em to db.
            """
            #self._push_to_db(tweets.get_user_timeline(user_id, count=50), "tweets")
            self._push_to_db(tweets.get_follower_list(user_id), "users")
            #self._push_to_db(tweets.get_friends_list(user_id), "users")

            time.sleep(CRAWLER_COLDDOWN_TIME)
            self.queue.put((int(time.time()), user_id))


class Analyzer(threading.Thread):

    def __init__(self, queue):
        super(Worker, self).__init__()
        db = pymongo.MongoClient(env.mongodb_url)["reylgan"]


    def is_zh(self, tweet):
        pass

    def extract_user(self, user_list):
        pass
    
    def run(self):
        pass
