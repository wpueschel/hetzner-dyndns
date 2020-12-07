#!/usr/bin/env python3

import sys
import yaml
import json
import requests

def main():
    # Check if we have a config file as argument
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    # Default config file
    else:
        config_file = "config.yaml"

    config = read_config(config_file)
    if config:
        config["external_ip"] = get_external_ip()
    else:
       sys.exit(1)

    config["zone_id"] = get_zone_id(config)
    config["record_id"], config["record_ip"] = get_record(config)

    print('{:<12} {}'.format("External IP:", config["external_ip"]))
    print('{:<12} {}'.format("Record IP:", config["record_ip"]))

    if config["external_ip"] == config["record_ip"]:
        print("Nothing to do.")
        sys.exit(0)

    if config["record_id"]:
        rt = update_record(config)
    else:
        rt = create_record(config)

    sys.exit(rt)


def read_config(config_file):
    try:
        cf = open(config_file, 'r')
        config = yaml.safe_load(cf)
        return config
    except FileNotFoundError as err:
        print("Config file not found:\n{}".format(err))
        return False
    except yaml.YAMLError as err:
            print("Could not read yaml:\n{}".format(err))
            return False


def get_external_ip():
    try:
        response = requests.get(url="https://api.ipify.org")
        external_ip = response.text
        return external_ip

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def get_zone_id(config):
    try:
        response = requests.get(
            url = config["zones_api_url"],
            headers = {"Auth-API-Token": config["access_token"]},
        )

        zones = json.loads(response.content)["zones"]

        for zone in zones:
            if zone["name"] == config["zone_name"]:
                print('{:<12} {}'.format("Zone ID:", zone["id"]))
                return (zone["id"])

        return False

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def get_record(config):
    try:
        response = requests.get(
            url = config["records_api_url"],
            params = {"zone_id": config["zone_id"]},
            headers = {"Auth-API-Token": config["access_token"]},
        )

        records = json.loads(response.content)["records"]

        for record in records:
            if record["name"] == config["record_name"]:
                print('{:<12} {}'.format("Record ID:",record["id"]))
                return record["id"], record["value"]

        return False, False

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def update_record(config):
    print("Updating record with new external IP {}:".format(config["external_ip"]))

    try:
        response = requests.put(
            url = config["records_api_url"] + "/" + config["record_id"],
            headers = {"Auth-API-Token": config["access_token"]},
            data = json.dumps({
                "value": config["external_ip"],
                "ttl": 600,
                "type": "A",
                "name": config["record_name"],
                "zone_id": config["zone_id"]
            })
        )

        if response.status_code != 200:
            print("Update failed with http_status_code: {}.".format(response.status_code))
            print("Response HTTP Response Body: {}".format(response.content))
            return response.status_code

        return 0

    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def create_record(config):

    print("CREATE")

    return 0

if __name__ == "__main__":
    main()

