# -*- coding: utf-8 -*-
"""
this module provide tweet fetching functions
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import time
import logging

import requests

from config import *


class Tweets(object):

    def __init__(self):
        self.session = requests.session()
        self.access_token = None

    def _handle_crawl_error(self):
        raise NotImplementedError

    def _obtain_access_token(self):
        """
        @todo token may get expired
        """
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
        """
        return a list of user
        """
        user_list = []
        next_cursor = -1
        while True:
            res = self.session.get(
                "%s?user_id=%s&cursor=%s" % (
                    TWITTER_FOLLOWER_LIST,
                    user_id,
                    next_cursor),
                headers={"Authorization": "Bearer %s" % self.access_token}
                ).json()
            if "errors" in res:
                # rate limited exceeded or Twitter dead
                logging.error(res["errors"])
                logging.info("waiting 1 hour...")
                time.sleep(3600)
            else:
                from pprint import pprint
                pprint (res)
                user_list.extend(res["users"])
                if "next_cursor" == -1:
                    break
                else:
                    cursor = res["next_cursor"]
        logging.info("fetch %s followers from user %s" % (len(user_list),
                                                          user_id))
        return user_list

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
