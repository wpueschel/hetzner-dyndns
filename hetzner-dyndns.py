#!/usr/bin/env python3

import yaml
import json
import requests

def main():

    config_file = "config.yml"
    config = read_config(config_file)
   
    config["external_ip"] = get_external_ip()
    config["zone_id"] = get_zone_id(config)
    config["record_id"], config["record_ip"] = get_record(config)


    print('{:<12} {}'.format("External IP:", config["external_ip"]))
    print('{:<12} {}'.format("Zone ID:", config["zone_id"]))
    print('{:<12} {}'.format("Record ID:", config["record_id"]))
    print('{:<12} {}'.format("Record IP:", config["record_ip"]))


def read_config(config_file):

    with open(config_file, 'r') as cf:
        try:
            config = yaml.safe_load(cf)
            return config
        except yaml.YAMLError as exc:
            print(exc)


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
                return (zone["id"])

        return ""

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
                return record["id"], record["value"]

        return ""

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def create_record(config):
    print("CREATE")


def update_record(config):
    print("UPDATE")


main()

exit()

