#!/usr/bin/env python
# coding=utf-8
import argparse
from sys import argv
from os import path
from os import stat
from mod import config
from mod.call import Call
from mod import state
from mod.schedule import Schedule
from mod.dal.dialstatus import Dialstatus
from mod.dal.carriers import Carriers
from mod.util import asterisk
from mod.util import phone
from mod.util import logger
from mod.util import audio
from multiprocessing import Process
from functools import partial

"""
Scan List of Numbers, lookup carrier, create Call File

"""
__author__ = 'Justin Zimmer'


def arguments():
    """ Primary Campaign Run Script """
    parser = argparse.ArgumentParser()
    # parser.add_argument('-c', '--channels', help="Number of channels to produce", default=2, type=int)
    # parser.add_argument('-b', '--bits', help="Number of bits in each sample", choices=(16,), default=16, type=int)
    # parser.add_argument('-r', '--rate', help="Sample rate in Hz", default=44100, type=int)
    # parser.add_argument('-t', '--time', help="Duration of the wave in seconds.", default=60, type=int)
    # parser.add_argument('-a', '--amplitude', help="Amplitude of the wave on a scale of 0.0-1.0.", default=0.5, type=float)
    # parser.add_argument('-f', '--frequency', help="Frequency of the wave in Hz", default=440.0, type=float)
    # parser.add_argument('filename', help="The file to generate.")
    return parser.parse_args()

def main():
    """
    Main Process
    """

    campaign, list_file = arguments()
    cfg = config.load_main()
    cfg.update(config.load_campaign(campaign))
    calls = {}
    if audio.test_file(cfg["vm_file"])[0] != "VERIFIED":
        exit(1)

    list_file = arguments()["listfile"]
    if not path.exists(list_file) or stat(list_file).st_size == 0:
        print """Specified file does not exist or is empty,
please check filename and try again!"""
        exit(1)
    with open(list_file) as leads:
        for line in leads:
            number = line.strip()
            if not number:
                print "Line is empty... what gives? Skipping..."
                continue
            print "Calling {0}".format(number)
            parsed_number = phone.lookup_number(phone.parse_phone(number), config)
            calls[parsed_number.e164] = Call(parsed_number, cfg)
            calls[parsed_number.e164].dialstatus = Dialstatus(
                config,
                list_file=list_file,
                vm_number=parsed_number.e164,
                campaign=cfg["campaign_code"],
                access_number=calls[parsed_number.e164].access_number,
                vm_file=cfg["vm_file"],
                dial_status='Spooling...',
                number_type=parsed_number.type)
    call_count = sum(call.vm_number.type == "mobile" for call in calls)
    sched = Schedule(call_count, cfg)
    for call in calls:
        if call.vm_number.type != "mobile":
            call.dialstatus.update(
                dial_status="Aborted",
                error="NOT MOBILE",
                error_text="This number is not a mobile number.")
            continue
        call_file = asterisk.file_innards(config, call)
        spool_file = asterisk.schedule_call(call_file, cfg, call, sched.next_timeslot_epoch())
        call.dialstatus.update(
            spool_file=spool_file,
            dial_status="Spooled")

if __name__ == '__main__':
    main()
