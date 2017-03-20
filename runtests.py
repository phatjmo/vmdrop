#!/usr/bin/env python
# coding=utf-8
import doctest
import argparse
from mod import call, config, schedule
from mod.util import audio, phone
"""
Run all the tests...
"""

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help="Display verbose output", default=False, action='store_const', const=True)
parser.add_argument('-r', '--report', help="Display Doctest report", default=False, action='store_const', const=True)
args = parser.parse_args()

def test_all():

    doctest.testmod(audio, verbose=args.verbose, report=args.report)
    doctest.testmod(schedule, verbose=args.verbose, report=args.report)

if __name__ == "__main__":
    test_all()
