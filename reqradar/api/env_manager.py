"""Load environment variables"""
# -*- coding: utf-8
__author__ = "Markel Elorza (0xBeppo)"
__version__ = "0.0.1"
__email__ = "eamarkel@gmail.com"
__status__ = "development"

from dotenv import load_dotenv
import os

class Env:
    def __init__(self):
        load_dotenv()
        self.token = os.environ.get('Sec')
        self.host = os.environ.get('Host')

    def get_sec(self):
        return self.token

    def get_host(self):
        return self.host

