#!/usr/bin/env python
# coding=utf-8
import json
import time
from sys import argv
from os import path
from os import stat
from multiprocessing import Process
from twilio.rest import TwilioRestClient
from functools import partial
"""
Insert Asterisk Node into Kamailio dispatcher.
"""
__author__ = 'JustinZimmer'


def arguments():
    if len(argv[1:]) < 2 or len(argv[1:]) > 3:
        print "Incorrect arguments.\n\nUsage:"
        "\n\t{0} NUMBERFILE ACTION (CONFIG)\n".format(path.basename(__file__))
        exit(1)
    elif len(argv[1:]) == 2:
        arguments = [argv[1], argv[2], 'cfgDict.json']
        print arguments
        return arguments
    else:
        arguments = [argv[1], argv[2], argv[3]]
        print arguments
        return arguments


def autodialer():
    numberFile, action, configfile = arguments()
    if not path.exists(numberFile) or stat(numberFile).st_size == 0:
        print """Specified file does not exist or is empty,
please check filename and try again!"""
        exit(1)
    cfgDict = {}
    if path.exists(configfile):
        try:
            cfgDict = json.load(open(configfile))
        except:
            print "{0} is invalid!\n".format(configfile)
            exit(1)
    else:
        makeNew = raw_input("""You are missing the necessary parameter file: {0}.\n
            Would you like to create a new one and manually enter parameters?
            (Y/N): """.format(configfile))
        if makeNew.strip()[0:1].upper() == 'Y':
            cfgDict = cfgParams(configfile)
        else:
            print "Oh well, I tried..."
            exit(1)
    maxconcurrent = int(cfgDict['maxconcurrent'])
    cps = float(cfgDict['cps'])
    batch = []
    interval = 1/cps
    partial_testpool = partial(
        testpool,
        ani=cfgDict['testani'],
        config=configfile,
        cps=cps
        )
    partial_makecall = partial(
        makecall,
        ani=cfgDict['testani'],
        accountsid=cfgDict['accountsid'],
        authtoken=cfgDict['authtoken']
        )
    with open(numberFile) as f:
        for line in f:
            number = line.strip()
            if not number:
                print "Line is empty... what gives? Skipping..."
                continue
            # print "Figuring out what to do with {0}...".format(number)
            if action.lower() == 'call':
                print "Calling {0}".format(number)
                process = Process(target=partial_makecall, args=(number,))
                process.start()
                batch.append(process)
                print "{0} has been pooled.".format(number)
                time.sleep(interval)
                if len(batch) >= maxconcurrent:
                    batch = cleanbatch(batch)
            elif action.lower() == 'test':
                process = Process(target=partial_testpool, args=(number,))
                process.start()
                batch.append(process)
                time.sleep(interval)
                if len(batch) >= maxconcurrent:
                    batch = cleanbatch(batch)
            else:
                print """You did not specify a valid action for this list.\n
                    Valid actions are: import, remove, enable, disable."""
                exit(1)
        while len(batch) > 0:
            print "Emptying batch"
            batch = cleanbatch(batch)
        print "Action: {0} for file: {1} has been completed!".format(
            action, numberFile)


def cleanbatch(batch):
    for proc in batch:
        proc.join()
        if not proc.is_alive():
            proc.terminate()
            batch.remove(proc)
            print "Batch now has {0} Processes.".format(
                len(batch)
            )
    return batch


def makecall(did, ani, accountsid, authtoken):
    # put your own credentials here
    ACCOUNT_SID = accountsid
    AUTH_TOKEN = authtoken

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    call = client.calls.create(
       url="http://demo.twilio.com/docs/voice.xml",
       to=did,
       from_=ani,
    )

    for x in range(0, 50):
        time.sleep(.100)
        call = client.calls.get(call.sid)
        if (
                call.status == 'in-progress' or
                call.status == 'busy' or
                call.status == 'completed' or
                call.status == 'failed' or
                call.status == 'no-answer' or
                call.status == 'canceled'
        ):
            threadtime = x*100
            print "Status for {0} is {1}, exiting thread after {2}ms.".format(
                did,
                call.status,
                threadtime
            )
            break

    call = client.calls.get(call.sid)
    if not (
            call.status == 'completed' or
            call.status == 'canceled'
    ):
        print "Status for {0} is still {1}, terminating!".format(
            did,
            call.status
            )
        call = client.calls.update(call.sid, status="completed")
    else:
        print "Status for {0} is {1}, call attempt is complete.".format(
                did,
                call.status
            )
    return call.status


def statcall(accountsid, authtoken, sid):

    # To find these visit https://www.twilio.com/user/account
    ACCOUNT_SID = accountsid
    AUTH_TOKEN = authtoken

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    message = client.calls.get(sid)
    return message.status


def hangcall(accountsid, authtoken, sid):

    # To find these visit https://www.twilio.com/user/account
    ACCOUNT_SID = accountsid
    AUTH_TOKEN = authtoken

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    message = client.calls.update(sid, status="completed")
    return message.status


def testpool(did, ani, config, cps):
    print "TEST!!! - Config File: {0}, Number: {1}, ANI: {2}, CPS: {3}".format(
            config,
            did,
            ani,
            cps
        )
    time.sleep(1)
    return "Complete"


def cfgParams(filename):
    cfgDict = {}
    cfgDict['testani'] = raw_input('Enter your Test Call ANI: ')
    cfgDict['accountsid'] = raw_input('Enter your Twilio AccountSID: ')
    cfgDict['authtoken'] = raw_input('Enter your Twilio AuthToken: ')
    cfgDict['cps'] = raw_input('Enter the max Calls Per Second: ')
    cfgDict['maxconcurrent'] = raw_input('Enter the max Concurrent Calls: ')
    json.dump(cfgDict, open(filename, 'w'))
    return cfgDict


if __name__ == '__main__':
    autodialer()
