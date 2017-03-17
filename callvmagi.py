#!/usr/bin/env python2.7
import sys
import time
from mod import config
from asterisk.agi import AGI

"""
Dial the voicemail access number for the customer's carrier and handle negative dial results.

"""
__author__ = 'Justin Zimmer'

main_config = config.load_main()

def call_vm():
    """ Call Voicemail Access Number and handle dial status..."""
    agi = AGI()
    agi.verbose("Calling voicemail access number...")
    vm_file = agi.get_variable('playfile')
    vm_number = agi.get_variable('vmnumber')
    access_number = agi.env['agi_extension']
    dial_string = "{0}/{1}/{2}".format(
        main_config["ast_tech"], main_config["ast_trunk"], access_number)
    agi.verbose("Dialing...")
    agi.execute("EXEC Dial", dial_string)
    time.sleep(3)
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


call_vm()