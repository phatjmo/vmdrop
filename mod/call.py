
import util
from mod.carriers import Carriers

class Call(object): # pylint: disable=too-few-public-methods
    """
    Object designed to hold individual call parameters.

    parsed_number is a modified PhoneNumber class containing the carrier and number type.

    -- Doctest --
    """
    def __init__(self, parsed_number, config):
        self.vm_number = parsed_number
        carriers = Carriers(config)
        self.access_number = carriers.get_access_number(
            parsed_number.carrier,
            str(parsed_number.national_number))
        #print "Access Number: {0}".format(self.access_number)

