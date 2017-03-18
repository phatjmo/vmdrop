#!/usr/bin/env python
# coding=utf-8
from sys import argv
from os import path
from mod import config
from mod import call
from mod import state
from mod.dal import dialstatus
from mod.dal import carriers
from mod.util import asterisk
from mod.util import phone
from mod.util import logger
from multiprocessing import Process
from functools import partial

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

def main():
    """ Primary Campaign Run Script """
    
    calls = {}
    number = "4803326545"
    parsed_number = parse_phone(number)
    calls[parsed_number.e164] = Call(parsed_number)

    number_file, action, config_file = arguments()
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


if __name__ == '__main__':
    main()