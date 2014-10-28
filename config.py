# -*- coding: utf-8 -*-
"""
this module provide basic configurations
"""
from environment import Environment


env = Environment(USER_AGENT=str,
                  CLIENT_KEY=str,
                  CLIENT_SECRET=str,
                  MONGODB_URL=str,
                  )

assert not any(_ in env.missing for _ in ["CLIENT_KEY", "CLIENT_SECRET", 
                                       "MONGODB_URL"])

TWITTER_API = "https://api.twitter.com"
TWITTER_OAUTH_URL = "%s/oauth2/token" % TWITTER_API
TWITTER_USER_TIMELINE = "%s/1.1/statuses/user_timeline.json" % TWITTER_API
TWITTER_FOLLOWER_LIST = "%s/1.1/followers/list.json" % TWITTER_API
TWITTER_FRIENDS_LIST = "%s/1.1/friends/list.json" % TWITTER_API
TWITTER_USER_INFO = "%s/1.1/users/lookup.json" % TWITTER_API

CRAWLER_COLDDOWN_TIME = 30
