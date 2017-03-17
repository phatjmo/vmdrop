
from twilio.rest.lookups import TwilioLookupsClient
"""
Utilities for managing phone number information and formatting.

"""
__author__ = 'Justin Zimmer'


def lookup_number(number, account_sid, auth_token):
    """Lookup carrier information for the specified phone number."""

    client = TwilioLookupsClient(account_sid, auth_token)
    try:
        response = client.phone_numbers.get(number, include_carrier_info=True)
        return response.carrier
    except TwilioRestException as error:
        if error.code == 20404:
            return False
        else:
            raise error
