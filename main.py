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

parser = argparse.ArgumentParser(
    description="Yet another tweet analyzer suite")
parser.add_argument("-w", "--worker",
                    help="amount of crawler",
                    type=int)
parser.add_argument("-f", "--frontend",
                    help="amount of frontend worker",
                    type=int)
parser.add_argument("-a", "--analyzer",
                    help="amount of analyzer.",
                    type=int)
parser.add_argument("--debug",
                    help="Debug model logging",
                    action="store_true")
parser.add_argument("-v", "--verbose",
                    help="Print log info into terminal",
                    action="store_true")
args = parser.parse_args()
queue = PriorityQueue()

def _init_queue():
    """
    add user_id from db
    queue.put((int(time.time()), user_id))
    """
    logging.info("queue initized")


def main(args):
    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG
    logging.basicConfig(filename=None if args.verbose else "reylgan.log",
                        #format="%(asctime)s:%(levelname)s: %(message)s",
                        level=log_level)
    if args.worker:
        _init_queue()
        try:
            crawler = [Worker(queue) for _ in range(0, int(args.worker))]
            [c.start() for c in crawler]
            logging.info("Started %s crawlers." % len(crawler))
            while True:
                for i in range(0, len(crawler)):
                    if not crawler[i].is_alive():
                        crawler[i] = Worker(queue)
                        logging.info(
                            "Starting a new worker %s" % crawler[i].name)
                        crawler[i].start()
                time.sleep(5)
        except KeyboardInterrupt:
            #for c in crawler:
            #    c.kill_received = True
            sys.exit(0)

    """
    raise analyzer
    """

    """
    raise frontend
    """


if __name__ == "__main__":
    main()
