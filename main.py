#!/usr/bin/env python
# coding=utf-8
import argparse
#from sys import argv
import csv
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
    """ Primary Campaign Run Script

    Example:

    ./main.py TEST examples/testlist.csv -c 1 -m 10 -v \
    examples/Nate_VM.wav -d MTWRF -t 09:00 -p 17:00

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('campaign',
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
    parser.add_argument('-D',
                        '--dump_csv',
                        help="Return phone number carrier and type export for list_file",
                        action='store_true')
    parser.add_argument('-P',
                        '--preprocessed',
                        help="This file has been pre-processed, skip Twilio queries",
                        action='store_true')
    return parser.parse_args()

def main():
    """
    Main Process
    """

    args = arguments().__dict__
    cfg = config.load_main()
    dump_csv = args.pop("dump_csv")
    query_twilio = True
    cfg.update(config.load_campaign(**args))
    calls = {}
    test_audio = audio.test_file(cfg["vm_file"])[0]
    if test_audio != "VERIFIED":
        print "There is something wrong with the audio file: {0}".format(test_audio)
        override_audio = raw_input("Do you want to run the file anyways? [Y/N]: ")
        if override_audio.strip()[0:1].upper() != 'Y':
            exit(1)

    ## Detect if file is dumpfile, check for carrier field, load using csv...
    list_file = args["list_file"]
    if not path.exists(list_file) or stat(list_file).st_size == 0:
        print """Specified file does not exist or is empty,
please check filename and try again!"""
        exit(1)
    with open(list_file, 'rb') as leads:
    ## Switch to CSV iterator
        reader = csv.DictReader(leads)
        headers = reader.fieldnames
        # Dumped number format: national_number,carrier,e164,country_code,type
        if 'carrier' in headers:
            print "File had already been processed, setting query_twilio to false"
            query_twilio = False
        
        for row in reader:
            number = row[0] # always first field or else!
            if not number:
                print "Line is empty... what gives? Skipping..."
                continue
            print "Calling {0}".format(number)
            if query_twilio:
                phone_number = Phone(number, sid=cfg["twilio_sid"], token=cfg["twilio_token"])
            else:
                phone_number = Phone(number, carrier=row["carrier"], type=row["type"])
            print "E.164: {0}, Carrier: {1}, Type: {2}".format(
                phone_number.e164,
                phone_number.carrier,
                phone_number.type)
            calls[phone_number.e164] = Call(phone_number, cfg)
            calls[phone_number.e164].dialstatus = Dialstatus(
                cfg,
                list_file=list_file,
                vm_number=phone_number.e164,
                campaign=cfg["campaign"],
                carrier=phone_number.carrier,
                access_number=calls[phone_number.e164].access_number,
                vm_file=cfg["vm_file"],
                dial_status='Spooling...',
                number_type=phone_number.type)

    if dump_csv:
        dump_list = [call.vm_number.__dict__ for key, call in calls.items()]
        headers = calls[enumerate(calls).next()[1]].vm_number.__dict__.keys()
        filename = "{0}.phonedump.csv".format(list_file)
        dump_to_csv(filename, headers, dump_list)
        exit(0)

    call_count = sum(calls[call].vm_number.type == "mobile" for call in calls)
    sched = Schedule(call_count, cfg)
    for call in calls:
        if calls[call].vm_number.type != "mobile":
            calls[call].dialstatus.update(
                dial_status="Aborted",
                error="NOT MOBILE",
                error_text="This number is not a mobile number.")
            continue
        call_file = asterisk.file_innards(cfg, calls[call])
        spool_file = asterisk.schedule_call(
            call_file,
            cfg,
            calls[call],
            sched.next_timeslot_epoch())
        calls[call].dialstatus.update(
            spool_file=spool_file,
            dial_status="Spooled")

def dump_to_csv(filename, header, dump_list):
    """
    Generate temp CSV file for the provided dictionary list.

    -- Doctest --

    """
    import csv

    with open(filename, 'w') as csvfile:
        fieldnames = header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for line in dump_list:
            writer.writerow(line)


if __name__ == '__main__':
    main()
