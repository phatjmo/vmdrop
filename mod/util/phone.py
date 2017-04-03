
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


def parse_phone(number, region="US"):
    """ Parse phone number into phone object """
    parsed_number = phonenumbers.parse(number, region)
    parsed_number.__dict__["e164"] = format_e164(parsed_number)
    return parsed_number

def format_e164(parsed_number):
    """ Parse and return e.164 phone number string. """
    return phonenumbers.format_number(parsed_number,
                                      phonenumbers.PhoneNumberFormat.E164)

def lookup_number(parsed_number, config):
    """Lookup carrier information for the specified phone number."""

    client = TwilioLookupsClient(config["twilio_sid"], config["twilio_token"])
    try:
        response = client.phone_numbers.get(parsed_number.e164, include_carrier_info=True)
        parsed_number.__dict__["carrier"] = response.carrier["name"]
        parsed_number.__dict__["type"] = response.carrier["type"]
        return parsed_number
    except TwilioRestException as error:
        if error.code == 20404:
            parsed_number.__dict__["carrier"]
            parsed_number.__dict__["type"]
            return parsed_number
        else:
            parsed_number.carrier = error.message
            parsed_number.type = error.code
            return parsed_number
