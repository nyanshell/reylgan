# -*- coding: utf-8 -*-
"""
"""

from __future__ import absolute_import, division, print_function, unicode_literals


def test_tweet_fetch():
    import main
    from argparse import Namespace
    args = Namespace(worker=1, verbose=True, debug=True)
    main.queue.put((1,769779572))
    main.main(args)


if __name__ == "__main__":
    test_tweet_fetch()
