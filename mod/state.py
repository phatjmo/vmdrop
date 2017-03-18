
class State(object):
    """ Current Run State for the campaign.
        Stores call and timestamp iterators.
    """

    def __init__(self, schedule_list, campaign_config):
        self.schedule = schedule_list