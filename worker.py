# -*- coding: utf-8 -*-
"""
this module controll db insertion
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import threading

import redis

from tweets import Tweets
from config import *


class Worker(threading.Thread):

    def run(self):
        redis_conn = redis.StrictRedis(host=env.redis_url,
                                       port=env.redis_port)
        


class Analyzer(threading.Thread):
    """
    """
    def is_zh(self, tweet):
        pass
    
    def run(self):
        pass
