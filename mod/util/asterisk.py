
from os import path
from os import utime
from shutil import move


"""
Helper functions for creating callfiles and managing Asterisk.

"""
__author__ = 'Justin Zimmer'



def file_innards(campaign, vm_number, access_number, caller_id, vm_file):
    """Generate Asterisk Call File in /tmp/, set mod time, and mv to spool path."""
    call_file = """
CallerID: {0}
Channel: Local/{1}@carriervmagi
Extension: {2}@vmdropagi 
Set: playfile={3},vmnumber={2},campaign={4}
""".format(caller_id, access_number, vm_number, vm_file, campaign)
    return call_file


def schedule_call(call_file, campaign, vm_number, call_time, spool_path):
    """
    Write Asterisk Call File in /tmp/, set mod time, and mv to spool path.
    call_file must be generated by file_innards before calling schedule.
    call_time must be a UNIX timestamp generated by mod.utils.future_time.
    """

    filename = "{0}_{1}_{2}.call".format(campaign, vm_number, call_time)
    temp_file = "/tmp/{0}".format(filename)
    spool_file = spool_path+"/"+filename
    handle = open(temp_file, "w")
    handle.write(call_file)
    handle.close()
    utime(temp_file, (call_time, call_time))
    move(temp_file, spool_file)






