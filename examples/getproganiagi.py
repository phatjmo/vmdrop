#!/usr/bin/env python2.7
import sys
from asterisk.agi import *
import MySQLdb
"""

Determine the Caller ID and Campaign Code based on the calling number. 
Start Recording and Make Call. 

"""
__author__ = 'Justin Zimmer'


def startAGI():
  agi = AGI()
  agi.verbose("UniDial PBX Dial Started...")
  xliteExt = agi.env['agi_callerid']
  dialedNum = agi.env['agi_extension']
  dbHost = agi.get_variable("UDDBHOST")
  dbUser = agi.get_variable("UDDBUSER")
  dbPass = agi.get_variable("UDDBPASS")
  dbDB = agi.get_variable("UDDB")
  agi.verbose("Collecting Caller ID and Campaign for %s" % xliteExt)
  try:
    agi.verbose("Connecting to: mysql://%s:%s@%s/%s..." % (dbUser, dbPass, dbHost, dbDB))
    db = MySQLdb.connect(host=dbHost, user=dbUser,
                         passwd=dbPass, db=dbDB)
  except:
    agi.verbose("I'm sorry, I couldn't connect to your database!")
    agi.stream_file('cannot-complete-network-error')
    agi.hangup()
    exit(1)

  c = db.cursor()
  c.execute("SELECT campaign, outani, emp_id FROM CELLANI WHERE xliteID=%s", [xliteExt])
  result = c.fetchone()
  if result is None:
    agi.verbose("Something went wrong!!! Result Empty! ABORT! ABORT!")
    c.close()
    db.close()
    agi.stream_file('cannot-complete-network-error')
    agi.hangup()
    exit(1)
  else:
    campaign = result[0]
    outANI = result[1]
    empID = result[2]
    agi.set_callerid(outANI)
    agi.set_variable("CAMPAIGN", campaign)
    agi.set_variable("EMPLOYEE", empID)
    agi.verbose("UniDial PBX Query complete: CAMPAIGN=%s, CALLERID(num)=%s, EMPLOYEE=%s" % (campaign, outANI, empID))
    sys.exit()


startAGI()
  # while True:
  #   # agi.stream_file('vm-extension')
  #   # result = agi.wait_for_digit(-1)
  #   # agi.verbose("got digit %s" % result)
  #   # if result.isdigit():
  #   #   agi.say_number(result)
  #   # else:
  #   #  agi.verbose("bye!")
  #   #  agi.hangup()
    
  #   sys.exit()