
from os import path
import json
"""
Manage configuration files for the main application and campaigns.

"""
__author__ = 'Justin Zimmer'


def load_main():
    """Load the main configuration for this instance."""
    config_file = "main_config.json"
    if path.exists(config_file):
        try:
            return load(config_file)
        except OSError as error:
            print "{0} is invalid because of {1}\n".format(config_file, error)
            exit(1)
    else:
        makenew = raw_input("""You are missing the necessary config file: {0}.\n
            Would you like to create a new one and manually enter parameters?
            (Y/N): """.format(config_file))

        if makenew.strip()[0:1].upper() == 'Y':
            main_config = build_main(config_file)
            save(main_config, config_file)
            return main_config
        else:
            print "Oh well, I tried..."
            exit(1)


def load_campaign(**config):
    """Load the specific config for this campaign."""

    if "campaign" not in config:
        config["campaign"] = raw_input(
            'You did not specify a campaign for this run! Please enter a campaign code: ')
        if config["campaign"] == '':
            print "I can't run this list without a campaign code!"
            exit(1)
    config_file = "config_{0}.json".format(config["campaign"])
    if path.exists(config_file):
        campaign_config = load(config_file)
    else:
        makenew = raw_input("""You are missing the necessary campaign file: {0}.\n
            Would you like to create a new one and manually enter parameters?
            (Y/N): """.format(config_file))
        if makenew.strip()[0:1].upper() == 'Y':
            campaign_config = build_campaign(**config)
        else:
            print "Oh well, I tried..."
            exit(1)
    save(campaign_config, config_file)
    return campaign_config


def save(cfgdict, config_file):
    """Save the specified config to the specified json file."""
    json.dump(cfgdict, open(config_file, 'w'))


def load(config_file):
    """load the specified json config file and return the dictionary."""
    try:
        return json.load(open(config_file))
    except OSError as error:
        print "{0} is invalid because of {1}\n".format(config_file, error)
        exit(1)


def build_main(config_file):
    """Build the main configuration file for this instance."""
    main_config = {}
    main_config['db_path'] = raw_input(
        'Enter the path to your database: [Enter for Default: database/]') or "database/"
    main_config['db_type'] = raw_input(
        'Enter the type of database you are using: [Enter for Default: sqlite3]') or "sqlite3"
    main_config['carrier_file'] = raw_input(
        'Carrier File to use when building carrier table (full path):') or "examples/testcarriers.csv"    
    main_config['ani'] = raw_input('Enter your Default Call ANI: ')
    main_config['twilio_sid'] = raw_input('Enter your Twilio AccountSID for this campaign: ')
    main_config['twilio_token'] = raw_input('Enter your Twilio AuthToken for this campaign: ')
    main_config['ast_spool'] = raw_input(
        "Enter this instance\'s Asterisk Spool path: "
        "[Enter for Default: /var/spool/asterisk/outgoing/] ") or "/var/spool/asterisk/outgoing/"
    main_config['ast_trunk'] = raw_input('Enter this instance\'s outbound trunk: ')
    main_config['ast_tech'] = raw_input(
        'Enter the technology type for this instance: [Enter for Default: SIP] ') or "SIP"
    save(main_config, config_file)
    return main_config


def build_campaign(**config):
    """Build the configuration file for this campaign."""
    campaign_config = {}
    campaign_config['campaign'] = config['campaign'] if 'campaign' in config else raw_input('Enter your Campaign Name: ')
    campaign_config['ani'] = config['ani'] if 'ani' in config else raw_input('Enter your Campaign Call ANI: ')
    campaign_config['cps'] = config['cps'] if 'cps' in config else raw_input('Enter the max Calls Per Second for this campaign: ')
    campaign_config['maxconcurrent'] = config['maxconcurrent'] if 'maxconcurrent' in config else raw_input(
        'Enter the max Concurrent Calls for this campaign: ')
    campaign_config['days_to_call'] = config['days_to_call'] if 'days_to_call' in config else raw_input(
        "Enter Stop Date for this Campaign "
        "(Mon = M, Tue = T, Wed = W, Thur = R, Fri = F, Sat = S, Sun = U): "
        "[Default: MTWRF] ") or "MTWRF"
    campaign_config['sched_start'] = config['sched_start'] if 'sched_start' in config else raw_input(
        'Enter Start Time for this Campaign (24HR - "HH:MM"): ')
    campaign_config['sched_stop'] = config['sched_stop'] if 'sched_stop' in config else raw_input(
        'Enter Start Time for this Campaign (24HR - "HH:MM"): ')
    campaign_config['vm_file'] = config['vm_file'] if 'vm_file' in config else raw_input(
        'Enter VM File for this Campaign (/full/path/to/file.wav): ')
    return campaign_config
