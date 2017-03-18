
import time
import datetime
from mod.util import audio

class Schedule(object):
    """
    Schedule object for the campaign run.

    Days of the Week: MTWRF
    Time: 00:00 - 23:59

    """

    # day_indexes = {}
    # day_indexes["M"] = 0
    # day_indexes["T"] = 1
    # day_indexes["W"] = 2
    # day_indexes["R"] = 3
    # day_indexes["F"] = 4
    # day_indexes["S"] = 5
    # day_indexes["U"] = 6

    days = []
    days[0] = "M"
    days[1] = "T"
    days[2] = "W"
    days[3] = "R"
    days[4] = "F"
    days[5] = "S"
    days[6] = "U"


    def __init__(self, call_list, campaign_config):
        self.job_start = datetime.datetime.today()
        self.days_to_call = list(campaign_config["days_to_call"])
        self.vm_length = audio.wav_duration(campaign_config["vm_file"])
        self.timeslots = []
        self.sched_start = self.make_time(campaign_config["sched_start"])
        self.sched_stop = self.make_time(campaign_config["sched_stop"])
        self.estimated_calltime = self.estimate_calltime()
        self.first_call = self.get_first_calltime(self.job_start)
        for call in call_list:

            datetime.datetime.today().strftime('%s')

    def next_day(self, date_time):
        """ Pull the next day. """
        n = 1
        while not self.match_dow(date_time+datetime.timedelta(days=n)):
            n += 1

        return datetime.datetime.combine(date_time+datetime.timedelta(days=n), self.sched_start)

    def match_dow(self, date_time):
        """ Is the date on the schedule? """
        if self.days[date_time.weekday()] in list(self.days_to_call):
            return True
        else:
            return False

    def within_sched(self, the_time):
        """
        Is the provided time within the allowed schedule?

        Using: datetime.time(9,0,0) <= datetime.datetime.now().time() <= datetime.time(23,0,0)

        """
        if self.sched_start <= the_time <= self.sched_stop:
            return True
        else:
            return False

    def make_time(self, time_string):
        """ Convert 24HR HH:MM timestring to datetime.time object. """
        time_pieces = time_string.split(":")
        hour = int(time_pieces[0])
        minute = int(time_pieces[1])
        return datetime.time(hour, minute)

    def get_epoch(self, date_time):
        """ Return UNIX Epoch for specified datetime (Only Unix). """
        return int(date_time.strftime('%s'))

    def estimate_calltime(self, call_setup=60):
        """ Estimate expected length of call to determine interval between timeslots. """
        return call_setup + self.vm_length

    def get_buffer(self, date_time, buffer=300):
        """ Round specified time and
        return with buffered start time to allow for processing."""
        round_time = date_time.replace(second=0, microsecond=0)
        buffed_time = round_time + datetime.datetime.timedelta(seconds=buffer)
        return buffed_time

    def get_first_calltime(self, date_time):
        """ Return first available calltime per schedule. """
        buffed_time = self.get_buffer(date_time)
        if not self.match_dow(buffed_time):
            return self.next_day(buffed_time)

        if buffed_time < self.sched_start:
            return datetime.datetime.combine(date_time+datetime.timedelta(days=n), self.sched_start)

        if buffed_time > self.sched_stop:
            return self.next_day(buffed_time)

        return buffed_time


