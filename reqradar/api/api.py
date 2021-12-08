"""API calls maker"""
# -*- coding: utf-8
__author__ = "Markel Elorza (0xBeppo)"
__version__ = "0.0.1"
__email__ = "eamarkel@gmail.com"
__status__ = "development"

import sys
import requests
import json
import os
import urllib
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
    """

    def __init__(self):
        self.headers = headers
        self.env = env_manager.Env()
        self.add_token()
        self.host = self.env.get_host()


    def add_token(self):
        self.headers['Sec'] = self.env.get_sec()
        return

    def get_log_sources(self):
        URL = f"https://{self.host}/api/config/event_sources/log_source_management/log_sources"

        response = requests.get(
            URL,
            headers=self.headers,
            verify=False
        )

        return response.json()


    def post_log_sources(self, name, description, host_source, log_source_type):
        """
        POST request to create a new log source based on the provided parameters

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
            "type_id": get_log_source_type_id(log_source_type),
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

        return response.json

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


