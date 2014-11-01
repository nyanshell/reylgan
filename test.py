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


def test_analyzer():
    """
    collection users need some data before test
    """
    import logging
    from queue import PriorityQueue
    from worker import Analyzer
    logging.basicConfig(filename=None,
                        level=logging.DEBUG)
    analyzer = Analyzer(PriorityQueue())
    analyzer.start()


def test_irrelevant_sub_regex():
    from worker import REPLACE_IRRELEVANT_REGEX
    s = "喵！喵1喵123喵喵喵!@#$%^&*abcdesAD1234http://tw.it"
    print (REPLACE_IRRELEVANT_REGEX.sub('', s))


if __name__ == "__main__":
    # test_tweet_fetch()
    # test_analyzer()
    test_irrelevant_sub_regex()
