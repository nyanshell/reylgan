# -*- coding: utf-8 -*-
"""
this module controll db insertion
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time
import logging
import re
import sys

import pymongo
from pymongo.errors import DuplicateKeyError

from tweets import Tweets
from config import *

if sys.version_info.major > 2:
    text_type = str
else:
    text_type = unicode


class Worker(threading.Thread):
    """
    @todo: Intends to use beanstalkd as queue, however beanstalkc didn't
    support py3k yet, use queue instead.
    While using PriorityQueue, user_id may get lost when thread crash.
    """
    def __init__(self, queue):
        super(Worker, self).__init__()
        self.queue = queue
        self.db = pymongo.MongoClient(env.mongodb_url)["reylgan"]
        self.daemon = True

    def _push_to_db(self, data, collect):
        """
        @todo upsert each user info
        """
        logging.info(
            "pushing %d items to collection %s." % (len(data), collect))
        try:
            self.db[collect].insert(data, continue_on_error=True)
        except  DuplicateKeyError as err:
            logging.warning(err)

    def run(self):
        tweets = Tweets()
        while True:
            user_id = self.queue.get()[-1]
            logging.info("fetching user %s." % user_id)
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


HTTP_REGEX_STR = '(https?://[\S]+)'
PUNCT_STR = ("([!@#\$%\^\&\*\(\)_\+\-=<>\/\:\"\';\|\\~!;,\.\?"
             "「」～！…（）；：，。？． ]+)")
REPLACE_IRRELEVANT_REGEX = re.compile("|".join([HTTP_REGEX_STR,
                                                PUNCT_STR,
                                                '([0-9]+)']))

class Analyzer(threading.Thread):
    def __init__(self, queue):
        super(Analyzer, self).__init__()
        self.db = pymongo.MongoClient(env.mongodb_url)["reylgan"]
        self.queue = queue
        self.daemon = True

    @staticmethod
    def detect_chinese(tweets, rate=0.5):
        """
        @todo: use a classifier model instead
        """
        def detect(text):
            s = REPLACE_IRRELEVANT_REGEX.sub(
                "",
                (text if isinstance(text, text_type)
                 else text.decode('utf-8')))
            # normal chinese character range [19968, 40908]
            cnt = sum([1 for _ in s if 19968 <= ord(_) <= 40908 ])
            return cnt/float(len(text))

        ans = 0
        assert len(tweets)
        for tweet in iter(tweets):
            if tweet['lang'] is 'zh': ans += 1.0
            # fix twitter's own language detect
            elif tweet['lang'] is 'ja':
                ans += detect(tweet['text'])
        ans /= float(len(tweets))
        return True if ans >= rate else False

    def run(self):
        logging.info("analyzer started")
        while True:
            logging.info("%s user_id in queue" % self.queue.qsize())
            cursor = self.db["users"].find(
                {"is_zh_user": True}).sort("followers_count",
                                           pymongo.DESCENDING)
            for user in cursor:
                logging.info("putting user %s to queue." % user["id"])
                self.queue.put((time.time(), user["id"]))

            cursor = self.db["users"].find(
                {"is_zh_user": False}).sort("followers_count",
                                           pymongo.DESCENDING)
