# -*- coding: utf-8 -*-
"""

"""
from __future__ import absolute_import, division, print_function, unicode_literals


import time
import argparse
import sys

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

def _init_queue():
    global queue
    queue = PriorityQueue()
    """
    add user_id from db
    queue.put((int(time.time()), user_id))
    """

def main():
    args = parser.parse_args()
    if args.worker:
        _init_queue()

        crawler = [Worker(queue) for _ in range(0, int(args.worker))]
        [c.start() for c in crawler]

        while True:
            for i in range(0, len(crawler)):
                if not crawler[i].is_alive():
                    crawler[i] = Worker(queue)
                    crawler[i].start()
            time.sleep(5)


if __name__ == "__main__":
    main()
