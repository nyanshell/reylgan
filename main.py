# -*- coding: utf-8 -*-
"""

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse

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
                    type=int,
                    require=True)


def main():
    args = parser.parse_args()
    crawlers = [Worker() for _ in range(0, args.worker)]
    while True:
        for crawler in crawlers:
            if not crawler.is_alive():
                crawler = Worker()
                crawler.start()

                
if __name__ == "__main__":
    main()
