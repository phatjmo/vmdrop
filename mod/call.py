
import util
import dal
from functools import partial

class Call(object): # pylint: disable=too-few-public-methods
    """
    Object designed to hold individual call parameters.

    parsed_number is a modified PhoneNumber class containing the carrier and number type.
    """

    def __init__(self, parsed_number, main_config, campaign_config):
        self.vm_number = parsed_number
        self.access_number = dal.carriers.get_access_number(parsed_number)
        


