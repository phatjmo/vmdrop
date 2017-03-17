#!/usr/bin/env python
# coding=utf-8
from sys import argv
from os import path
from mod import config
from mod.dal import dialstatus
from mod.dal import carriers
from mod.util import asterisk
from mod.util import phone
from mod.util import logger

"""
Scan List of Numbers, lookup carrier, create Call File

"""
__author__ = 'Justin Zimmer'


def arguments():
    if len(argv[1:]) < 1 or len(argv[1:]) > 1:
        print "Incorrect arguments.\n\nUsage:"
        "\n\t{0} Number\n".format(path.basename(__file__))
        exit(1)
    else:
        arguments = argv[1]
        print arguments
        return arguments