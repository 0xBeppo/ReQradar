"""API calls maker"""
# -*- coding: utf-8
__author__ = "Markel Elorza (0xBeppo)"
__version__ = "0.0.1"
__email__ = "eamarkel@gmail.com"
__status__ = "development"

import sys
import time
import requests
import json
import os
import urllib
import urllib3
import env_manager

HEADERS = {
    'Accept': 'application/json',
    'Version': '12.0',
    'Content-Type': 'application/json'
}
class API:
    """
    A class used to perform querys to the Qradar API

    ...

    Attributes
    ----------
    HEADERS / headers: dict
        Dictionary with the default headers for the API call

    Methods
    -------
    get_log_sources()
        GET request to fetch all log sources
    get_log_source_type_id(log_source_type) : int
        GET request to get the id of the ID of specific log source
    post_log_sources(name, description, host_source, log_source_type)
        POST request to create a new log source based on the provided parameters
    post_deploy(self, deploy_type="INCREMENTAL")
        POST request to deploy changes in Qradar
        POST - /staged_config/deploy_status
    """

    def __init__(self):
        self.headers = HEADERS
        self.env = env_manager.Env()
        self.add_token()
        self.host = self.env.get_host()
        self.deploy_needed = False
        urllib3.disable_warnings()


    def add_token(self):
        self.headers['Sec'] = self.env.get_sec()
        return


    def check_deploy(self, data):
        if "requires_deploy" in data:
            if data['requires_deploy'] == True:
                self.deploy_needed = True
        return

    def get_deploy_needed(self):
        return self.deploy_needed


    def get_log_sources(self):
        """
        GET request to fetch all log sources. Also changes deploy_needed to true if some of the sources needs to be deployed
        """
        URL = f"https://{self.host}/api/config/event_sources/log_source_management/log_sources"

        response = requests.get(
            URL,
            headers=self.headers,
            verify=False
        )

        log_sources = response.json()
        for log_source in log_sources:
            self.check_deploy(log_source)

        return log_sources


    def post_log_sources(self, name, description, host_source, log_source_type):
        """
        POST request to create a new log source based on the provided parameters.
        Changes deploy_needed to True if the source needs to be deployed

        Parameters
        ----------
        name : str
            Name of the new Log Source
        description : str
            Description of the new Log Source
        host_source : str
            The IPv4 or hostname that identifies the log source (Origin of this log source)
        log_source_type : str
            Name of the log source type. Must correspond to an existing log source type
        """

        URL = f"https://{self.host}/api/config/event_sources/log_source_management/log_sources"
        params = {
            "name": name,
            "description": description,
            "type_id": self.get_log_source_type_id(log_source_type),
            "protocol_type_id": 0,
            "protocol_parameters": [
                {
                    "name": "incomingPayloadEncoding",
                    "id": 1,
                    "value": "UTF-8"
                },
                {
                    "name": "identifier",
                    "id": 0,
                    "value": host_source
                }
            ],
            "enabled": True,
            "credibility": 5,
            "target_event_collector_id": 7,
            "coalesce_events": True,
            "store_event_payload": True,
            "group_ids": [
                0
            ]
        }
        response = requests.post(
            URL,
            headers = self.headers,
            json = params,
            verify = False
        )

        log_source = response.json()
        self.check_deploy(log_source)

        return log_source


    def get_log_source_type_id(self, log_source_type):
        """
        GET request to get the id of the ID of specific log source

        Parameters
        ----------
        log_source_type : str
            Name of the log source type. Must correspond to an existing log source type
        """

        params = f'name="{log_source_type}"'
        encoded_params = urllib.parse.quote(params)
        URL = f"https://{self.host}/api/config/event_sources/log_source_management/log_source_types?filter={encoded_params}"

        response = requests.get(
            URL,
            headers=self.headers,
            verify=False
        )

        log_source = response.json()

        return log_source[0]['id']

    #TODO
    #Log sources Delete and Update

    def post_deploy(self, deploy_type="INCREMENTAL", force=False): #TODO improve documentation (Errors)
        """
        POST request to deploy changes in Qradar
        POST - /staged_config/deploy_status

        Parameters
        ----------
        deploy_type : str
            Type of the deploy, should be either INCREMENTAL or FULL
        force: bool
            Force the deployment even if deploy_needed is False
        """
        URL = f"https://{self.host}/api/staged_config/deploy_status"
        print(deploy_type)

        if deploy_type != "INCREMENTAL" and deploy_type != "FULL":
            print("[!] ERROR: Deploy type should be either INCREMENTAL or FULL")
            return

        if self.deploy_needed == False and force != True:
            print("[!] ERROR: No changes to deploy")
            return

        response = requests.post(
            URL,
            headers = self.headers,
            json = {"type": deploy_type},
            verify = False
        )

        if response.status_code != 200:
            print("[!] ERROR, something went wrong!")
            return

        #TODO Make req to deploy_status till status not IN_PROGRESS
        status = self.get_deploy_status()
        while status != "COMPLETE":
            print("[*] Deploy in progress...")
            time.sleep(3)
            status = self.get_deploy_status()

        print("[+] Deploy completed!")

        return


    def get_deploy_status(self):
        URL = f"https://{self.host}/api/staged_config/deploy_status"

        response = requests.get(
            URL,
            headers = self.headers,
            verify = False
        )

        deploy_status = response.json()
        return deploy_status['status']


