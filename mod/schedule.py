
import time
import timestamp

class Schedule(object):
    """ 
    Schedule object for the campaign run.

    Days of the Week: MTWRF
    Time: 00:00 - 23:59

    """

    day_indexes = {}
    day_indexes["M"] = 0
    day_indexes["T"] = 1
    day_indexes["W"] = 2
    day_indexes["R"] = 3
    day_indexes["F"] = 4
    day_indexes["S"] = 5
    day_indexes["U"] = 6

    def __init__(self, call_list, campaign_config):
        for call in call_list:
            self.job_start = datetime.datetime.today()
            days_to_call = list(campaign_config["days_to_call"])
            
            datetime.datetime.today().strftime('%')
    
    def next_day():
        """ Pull the next day. """

    def match_dow(self, days_to_call, date_time):
        """ Is the date on the schedule? """
        for day in list(days_to_call):
            if date_time.weekday() == day_indexes[day]:
                return True
            
        return False

            
            

