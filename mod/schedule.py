
import time
import datetime
import itertools
from mod.util import audio

class Schedule(object):
    """
    Schedule object for the campaign run.

    Days of the Week: MTWRF
    Time: 00:00 - 23:59

    -- Doctest --
    >>> import os
    >>> import datetime
    >>> from mod.util import audio
    >>> campaign = {"days_to_call": "MTWRF", "sched_start": "09:00", "sched_start": "09:00", "sched_stop": "17:00", "cps": 2, "maxconcurrent": 5, "vm_file": audio.make_test_wav()}
    >>> sched = Schedule(10, campaign, datetime.datetime(2017, 3, 17, 9, 0))
    >>> [sched.next_timeslot_epoch() for __call in range(sched.call_count)]
    [1489766700, 1489766700, 1489766701, 1489766701, 1489766701, 1489766792, 1489766792, 1489766792, 1489766883, 1489766883]
    >>> sched.next_timeslot_epoch()
    Traceback (most recent call last):
        ...
    StopIteration
    >>> sched.gen_timeslot()
    datetime.datetime(2017, 3, 17, 9, 8, 3)
    >>> os.remove(campaign["vm_file"])
    """

    # day_indexes = {}
    # day_indexes["M"] = 0
    # day_indexes["T"] = 1
    # day_indexes["W"] = 2
    # day_indexes["R"] = 3
    # day_indexes["F"] = 4
    # day_indexes["S"] = 5
    # day_indexes["U"] = 6

    days = list("MTWRFSU")

    def __init__(self, call_count, config, job_start=datetime.datetime.today()):
        self.job_start = job_start # datetime.datetime.today()
        self.days_to_call = list(config["days_to_call"])
        self.vm_length = audio.wav_duration(config["vm_file"])
        self.sched_start = self.make_time(config["sched_start"])
        self.sched_stop = self.make_time(config["sched_stop"])
        self.estimated_calltime = self.estimate_calltime()
        self.first_calltime = self.get_first_calltime()
        self.current_calltime = self.first_calltime
        self.cps = config["cps"]
        self.maxconcurrent = config["maxconcurrent"]
        self.cps_counter = self.reset_counter(self.cps)
        self.concurrent_counter = self.reset_counter(self.maxconcurrent)
        self.call_count = call_count
        self.call_counter = self.reset_counter(self.call_count)
        self.timeslots = iter([self.gen_timeslot() for __call in range(call_count)])


    def gen_timeslot(self):
        """
        Pull timeslot entry for Schedule
        """
        try:
            next(self.cps_counter)
        except StopIteration:
            self.current_calltime = self.get_next_calltime(1)
            self.cps_counter = self.reset_counter(self.cps)

        try:
            next(self.concurrent_counter)
        except StopIteration:
            self.current_calltime = self.get_next_calltime()
            self.concurrent_counter = self.reset_counter(self.cps)

        return self.current_calltime

    def next_timeslot_epoch(self):
        """ return the next timeslot as UNIX Epoch """
        try:
            return self.get_epoch(next(self.timeslots))
        except StopIteration as stop:
            raise stop

    def reset_counter(self, count):
        """ Return new counter based on count. """
        return itertools.islice(itertools.count(1, 1), count)

    def get_next_day(self, date_time):
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

    def get_buffer(self, date_time, buff=300):
        """ Round specified time and
        return with buffered start time to allow for processing."""
        round_time = date_time.replace(second=0, microsecond=0)
        buffed_time = round_time + datetime.timedelta(seconds=buff)
        return buffed_time

    def get_first_calltime(self):
        """ Return first available calltime per schedule. """
        buffed_time = self.get_buffer(self.job_start)
        if not self.match_dow(buffed_time):
            return self.get_next_day(buffed_time)

        if buffed_time.time() < self.sched_start:
            return datetime.datetime.combine(buffed_time, self.sched_start)

        if buffed_time.time() >= self.sched_stop:
            return self.get_next_day(buffed_time)

        return buffed_time

    def get_next_calltime(self, interval=None):
        """ Return next timeslot based on current_calltime and estimated_calltime (interval). """
        if interval is None:
            interval = self.estimated_calltime
        next_calltime = self.current_calltime + datetime.timedelta(seconds=interval)
        if not self.match_dow(next_calltime):
            return self.get_next_day(next_calltime)

        if next_calltime.time() < self.sched_start:
            return datetime.datetime.combine(next_calltime, self.sched_start)

        if next_calltime.time() >= self.sched_stop:
            return self.get_next_day(next_calltime)

        return next_calltime


if __name__ == "__main__":
    import doctest
    doctest.testmod()
