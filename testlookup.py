#!/usr/bin/env python
# coding=utf-8
from twilio.rest.lookups import TwilioLookupsClient
from sys import argv
from os import path

"""
Test Twilio REST API.

Very Helpful:

https://www.twilio.com/blog/2016/02/how-to-verify-phone-numbers-in-python-with-the-twilio-lookup-api.html

"""
__author__ = 'JustinZimmer'


def arguments():
    if len(argv[1:]) < 1 or len(argv[1:]) > 1:
        print "Incorrect arguments.\n\nUsage:"
        "\n\t{0} Number\n".format(path.basename(__file__))
        exit(1)
    else:
        arguments = argv[1]
        print arguments
        return arguments

lookup = arguments()
account_sid = "SK4faa39d383504948bd946ca2945c5e77" # Your Account SID from www.twilio.com/console
auth_token  = "jjgXmkNKVnKJGXXp348k4ETLksHciCL5"  # Your Auth Token from www.twilio.com/console

client = TwilioLookupsClient(account_sid, auth_token)

number = client.phone_numbers.get(lookup, include_carrier_info=True)

print("This is a {0} number belonging to {1}".format(number.carrier["type"], number.carrier["name"]))
