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
    print(api.get_log_sources())

if __name__ == "__main__":
    run()
