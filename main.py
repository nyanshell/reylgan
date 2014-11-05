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
parser.add_argument("-a", "--analyzer",
                    help="amount of analyzer",
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
    workers = []
    if args.worker:
        workers.extend([(Worker(), Worker) for _ in
                        range(0, int(args.worker))])
        logging.info("add %s crawlers." % args.worker)

    if args.analyzer:
        workers.extend([(Analyzer(), Analyzer) for _ in
                        range(0, int(args.analyzer))])
        logging.info("add %s analyzers." % args.analyzer)

    if args.frontend:
        """
        @todo: start frontend worker
        """
        raise NotImplementedError

    [w[0].start() for w in workers]
        
    while True:
        for i, worker in enumerate(workers):
            if not worker[0].is_alive():
                    worker[0] = worker[1]()
                    logging.info(
                        "Starting a new worker %s" % worker[0].name)
                    worker[0].start()
        time.sleep(5)



if __name__ == "__main__":
    main(args)
