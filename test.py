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
    logging.basicConfig(level=logging.DEBUG)
    analyzer = Analyzer(PriorityQueue())
    analyzer.start()
    analyzer.join()


def test_irrelevant_sub_regex():
    from worker import REPLACE_IRRELEVANT_REGEX
    s = "喵！喵1喵123喵喵喵!@#$%^&*abcdesAD1234http://tw.it"
    assert REPLACE_IRRELEVANT_REGEX.sub('', s) == "喵喵喵喵喵喵abcdesAD"


def test_chinese_detect():
    from worker import Analyzer
    detect = Analyzer.detect_chinese
    assert (detect([{"text": "喵！喵1臺灣烏龜123", "lang": "ja"},
                   {"text": "asdfasdfa", "lang": "ja"},
                   {"text": "喵喵喵喵喵喵", "lang": "ja"}]))


if __name__ == "__main__":
    # test_tweet_fetch()
    test_analyzer()
    # test_irrelevant_sub_regex()
    # test_chinese_detect()
