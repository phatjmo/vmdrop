
import phonenumbers
from twilio.rest.lookups import TwilioLookupsClient
from twilio.rest.exceptions import TwilioRestException
"""
Utilities for managing phone number information and formatting.

API returns:

{
    "url": "https://lookups.twilio.com/v1/PhoneNumbers/+15108675309?Type=carrier",
    "carrier": {
        "error_code": null,
        "type": "mobile",
        "name": "T-Mobile USA, Inc.",
        "mobile_network_code": "160",
        "mobile_country_code": "310"
    },
    "national_format": "(510) 867-5309",
    "phone_number": "+15108675309",
    "country_code": "US"
}

"""
__author__ = 'Justin Zimmer'

class Phone(object):
    """ Custom class for storing pertinent phone information. """
    def __init__(self, phone_number, **kwargs):
        parsed_phone = self.parse_phone(phone_number)
        self.e164 = self.format_e164(parsed_phone)
        self.national_number = parsed_phone.national_number
        self.country_code = parsed_phone.country_code
        self.lookup_number(kwargs["sid"], kwargs["token"])

    def parse_phone(self, number, region="US"):
        """ Parse phone number into phone object """
        parsed_number = phonenumbers.parse(number, region)
        return parsed_number

    def format_e164(self, parsed_number):
        """ Parse and return e.164 phone number string. """
        return phonenumbers.format_number(parsed_number,
                                          phonenumbers.PhoneNumberFormat.E164)

    def lookup_number(self, sid, token):
        """Lookup carrier information for the specified phone number."""

        client = TwilioLookupsClient(sid, token)
        try:
            response = client.phone_numbers.get(self.e164, include_carrier_info=True)
            self.carrier = response.carrier["name"]
            self.type = response.carrier["type"]
        except TwilioRestException as error:
            if error.code == 20404:
                self.carrier = 'None'
                self.type = 'Invalid'
            else:
                self.carrier = error.message
                self.type = error.code
