# -*- coding: utf-8 -*-
"""
this module provide tweet fetching functions
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import requests

from config import *


class Tweets(object):

    def __init__(self):
        self.session = requests.session()
        self.access_token = None

    def _obtain_access_token(self):
        encoded_bearer = base64.b64encode(('%s:%s' % (
                env.client_key, env.client_secret)).encode("utf-8"))
        headers = {"User-Agent": env.user_agent,
                   "Authorization": "Basic %s" % encoded_bearer.decode(
                "utf-8"),
                   "Content-Type": "application/x-www-form-urlencoded;"
                   "charset=UTF-8",
                   "Accept-Encoding": "gzip"}
        res = self.session.post(TWITTER_OAUTH_URL,
                           headers=headers,
                           data="grant_type=client_credentials")
        assert res.status_code == 200
        return res.json()["access_token"]

    def ensure_access_token(f):
        def wrapper(self, *args, **kwargs):
            if not self.access_token:
                self.access_token = self._obtain_access_token()
            return f(self, *args, **kwargs)
        return wrapper

    @ensure_access_token
    def get_user_timeline(self, user_id, count=20):
        res = self.session.get(
            "%s?user_id=%s&count=%s" % (TWITTER_USER_TIMELINE,
                                        user_id,
                                        count),
            headers={"Authorization": "Bearer %s" % self.access_token})
        return res.json()

    @ensure_access_token
    def get_follower_list(self, user_id):
        res = self.session.get(
            "%s?user_id=%s" % (TWITTER_FOLLOWER_LIST,
                               user_id,
                               count),
            headers={"Authorization": "Bearer %s" % self.access_token})
        return res.json()

    @ensure_access_token
    def get_friends_list(self, user_id):
        res = self.session.get(
            "%s?user_id=%s" % (TWITTER_FRIENDS_LIST,
                               user_id),
            headers={"Authorization": "Bearer %s" % self.access_token})
        return res.json()

    @ensure_access_token
    def get_friends_list(self, user_id):
        res = self.session.get(
            "%s?user_id=%s" % (TWITTER_FRIENDS_LIST,
                               user_id),
            headers={"Authorization": "Bearer %s" % self.access_token})
        return res.json()


if __name__ == "__main__":
    tweets = Tweets()
    print (tweets.get_user_timeline(user_id=115763683, count=1))
