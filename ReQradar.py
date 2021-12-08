#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Python App for managing Qradar
   Aims the automatization of Qradar administration
"""

__author__ = "Markel Elorza (0xBeppo)"
__version__ = "0.0.1"
__email__ = "eamarkel@gmail.com"
__status__ = "development"

from api import API

def run():
    api = API()
    api.post_log_sources("webserverRsyslog", "Rsyslog source of webserver", "webserver", "Linux OS")
    api.post_log_sources("databaseRsyslog", "Rsyslog source of database", "database", "Linux OS")
    api.post_log_sources("firewallRsyslog", "Rsyslog source of firewall", "firewall", "Linux OS")
    api.post_log_sources("rabbitmqRsyslog", "Rsyslog source of rabbitmq", "rabbitmq", "Linux OS")
    api.post_deploy()

if __name__ == "__main__":
    run()
