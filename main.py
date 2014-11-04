# -*- coding: utf-8 -*-
"""

"""
from __future__ import absolute_import, division, print_function, unicode_literals


import time
import argparse
import sys
import logging

if sys.version_info.major > 2:
    from queue import PriorityQueue
else:
    from Queue import PriorityQueue

from worker import Worker
from worker import Analyzer

parser = argparse.ArgumentParser(
    description="Yet another tweet analyzer suite")
parser.add_argument("-w", "--worker",
                    help="amount of crawler",
                    type=int)
parser.add_argument("-f", "--frontend",
                    help="amount of frontend worker",
                    type=int)
parser.add_argument("--debug",
                    help="Debug model logging",
                    action="store_true")
parser.add_argument("-v", "--verbose",
                    help="Print log info into terminal",
                    action="store_true")
args = parser.parse_args()


def main(args):
    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG
    logging.basicConfig(filename=None if args.verbose else "reylgan.log",
                        level=log_level)
    if args.worker:
        analyzer = Analyzer()
        analyzer.start()
        crawler = [Worker() for _ in range(0, int(args.worker))]
        [c.start() for c in crawler]
        logging.info("Started %s crawlers." % len(crawler))
        while True:
            for i in range(0, len(crawler)):
                if not crawler[i].is_alive():
                    crawler[i] = Worker()
                    logging.info(
                        "Starting a new worker %s" % crawler[i].name)
                    crawler[i].start()
            analyzer = Analyzer() if not analyzer.is_alive() \
                       else analyzer
            time.sleep(5)
    if args.frontend:
        """
        @todo: start frontend worker
        """
        raise NotImplementedError


if __name__ == "__main__":
    main()
