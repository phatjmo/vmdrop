#!/usr/bin/env python2.7
import sys
import time
from mod import config
from asterisk.agi import AGI

"""
Play DTMF on answer and then streamfile after a second of silence.

"""
__author__ = 'Justin Zimmer'

main_config = config.load_main()

def vm_drop():
    """ Call Voicemail Access Number and handle dial status..."""
    agi = AGI()
    agi.verbose("Calling voicemail access number...")
    vm_file = agi.get_variable('playfile')
    vm_number = agi.get_variable('vmnumber')
    access_number = agi.env['agi_extension']
    time.sleep(3)
    agi.execute("EXEC WaitForNoise", "1000")
    agi.execute("EXEC SendDTMF", vm_number)
    agi.execute("EXEC WaitForSilence", "2000")
    agi.verbose("Something went wrong!!! Result Empty! ABORT! ABORT!")
    agi.stream_file(vm_file)
    agi.hangup()
    exit(1)

# campaign = result[0]
# outANI = result[1]
# empID = result[2]
# agi.set_callerid(outANI)
# agi.set_variable("CAMPAIGN", campaign)
# agi.set_variable("EMPLOYEE", empID)
# agi.verbose("UniDial PBX Query complete: CAMPAIGN=%s, CALLERID(num)=%s, EMPLOYEE=%s" % (campaign, outANI, empID))
# sys.exit()


vm_drop()