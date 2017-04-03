#!/usr/bin/env python
# coding=utf-8
import argparse
#from sys import argv
from os import path
from os import stat
from mod import config
from mod.call import Call

from mod.schedule import Schedule
from mod.dialstatus import Dialstatus
#from mod.carriers import Carriers
from mod.util import asterisk
from mod.util.phone import Phone
#from mod.util import logger
from mod.util import audio
#from multiprocessing import Process
#from functools import partial

"""
Scan List of Numbers, lookup carrier, create Call File

"""
__author__ = 'Justin Zimmer'


def arguments():
    """ Primary Campaign Run Script """
    parser = argparse.ArgumentParser()
    parser.add_argument('campaign_code',
                        help="Shortcode for this call campaign", type=str)
    parser.add_argument('list_file',
                        help="The list file to call.", type=str)
    parser.add_argument('-c',
                        '--cps',
                        help="Max calls in one second", type=int)
    parser.add_argument('-m',
                        '--maxconcurrent',
                        help="Max calls at one time (max channels)", type=int)
    parser.add_argument('-v',
                        '--vm_file',
                        help="Full path to voicemail file to play.", type=str)
    parser.add_argument('-d',
                        '--days_to_call',
                        help="Days of the week for this list to call.", type=str)
    parser.add_argument('-t',
                        '--sched_start',
                        help="Time of day for calling to start", type=str)
    parser.add_argument('-p',
                        '--sched_stop',
                        help="Time of day for calling to stop", type=str)
    return parser.parse_args()

def main():
    """
    Main Process
    """

    args = arguments().__dict__
    cfg = config.load_main()
    cfg.update(config.load_campaign(**args))
    calls = {}
    test_audio = audio.test_file(cfg["vm_file"])[0]
    if test_audio != "VERIFIED":
        print "There is something wrong with the audio file: {0}".format(test_audio)
        override_audio = raw_input("Do you want to run the file anyways? [Y/N]: ")
        if override_audio.strip()[0:1].upper() != 'Y':
            exit(1)

    list_file = args["list_file"]
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
            phone_number = Phone(number, sid=cfg["twilio_sid"], token=cfg["twilio_token"])
            print "E.164: {0}, Carrier: {1}, Type: {2}".format(
                phone_number.e164,
                phone_number.carrier,
                phone_number.type)
            calls[phone_number.e164] = Call(phone_number, cfg)
            calls[phone_number.e164].dialstatus = Dialstatus(
                config,
                list_file=list_file,
                vm_number=phone_number.e164,
                campaign_code=cfg["campaign_code"],
                access_number=calls[phone_number.e164].access_number,
                vm_file=cfg["vm_file"],
                dial_status='Spooling...',
                number_type=phone_number.type)
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
