#!/usr/bin/env python

import yaml
import requests

def main():

    config_file = "config.yml"
    config = read_config(config_file)


# Read config file
def read_config(config_file):
    with open(config_file, 'r') as cf:
        try:
            config = yaml.safe_load(cf)
        except yaml.YAMLError as exc:
            print(exc)
    return config

def get_zone_id:


def get_record:


def create_record:


def update_record:


main()

exit()

