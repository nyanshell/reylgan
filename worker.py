# -*- coding: utf-8 -*-
"""
this module controll db insertion
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time
import logging
import re

import pymongo
from pymongo.errors import DuplicateKeyError

from tweets import Tweets
from config import *


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
                                                '([a-zA-Z0-9]+)']))

class Analyzer(threading.Thread):
    def __init__(self, queue):
        super(Analyzer, self).__init__()
        self.db = pymongo.MongoClient(env.mongodb_url)["reylgan"]
        self.queue = queue
        self.daemon = True

    def detect_chinese(tweets, rate=0.7):
        """
        @todo: use a classifier model instead
        """
        def detect(rs):
            if isinstance(rs, unicode):
                s = rs
            else:
                s = rs.decode('utf-8')
            s = HTTP_SUB_REGEX.sub('', s)
            s = PUNCT_CHAR_SUB.sub('', s)
            tot_chr = len( EN_WORDS_SUB_REGEX.findall(s))
            s = EN_WORDS_SUB_REGEX.sub('', s)
            zh_chr = 0
            for c in s:
                tot_chr += 1
                # normal chinese character range [19968, 40908]
                if 19968 <= ord(c) <= 40908:
                    zh_chr += 1
                    rate = 0.00000
                    if tot_chr != 0:
                        rate = float(zh_chr)/tot_chr
                    return rate 

        ans = 0.0000
        cnt = len(tweets)
        assert cnt
        if tweet[ 'lang' ] == 'zh':
            ans += 1.000
        elif tweet[ 'lang' ] == 'ja': # fix twitter's own language detect
            tr = zhdetect( tweet[ 'text' ] )
            ans += tr
        if cnt > 0:
            ans /= float(cnt)
            if ans >= rate:
                return True
        return False

    def run(self):
        logging.info("analyzer started")
        while True:
            print ("size", self.queue.qsize())
            cursor = self.db["users"].find(
                {"is_zh_user": True}).sort("followers_count",
                                           pymongo.DESCENDING)
            for user in cursor:
                logging.info("putting user %s to queue." % user["id"])
                self.queue.put((time.time(), user["id"]))

            cursor = self.db["users"].find(
                {"is_zh_user": False}).sort("followers_count",
                                           pymongo.DESCENDING)
