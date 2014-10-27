# -*- coding: utf-8 -*-
"""
this module controll db insertion
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time

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
        super(Worker, self).__init__()

    def run(self):
        while True:
            user_id = self.queue.get()[-1]
            """
            print (self.name, user_id)
            pull tweet, user's follower & friends
            push em to db.
            """
            time.sleep(CRAWLER_COLDDOWN_TIME)
            self.queue.put((int(time.time()), user_id))


class Analyzer(threading.Thread):
    """
    """
    def is_zh(self, tweet):
        pass
    
    def run(self):
        pass
