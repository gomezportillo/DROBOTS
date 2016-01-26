#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
import math
Ice.loadSlice('./Container.ice  --all -I .')
import drobots 
#from RobotFactory import RobotFactory
from collections import namedtuple

from Client import *
from Player import *
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#Guarda proxies de controler, no de robots
class Container:
    def __init__(self):
        self.proxies = dict()

    def link(self, key, proxy):
        if key in self.proxies:
            raise Services.AlreadyExists(key)

        print("link: {0} -> {1}".format(key, proxy))
        self.proxies[key] = proxy

    def unlink(self, key):
        if not key in self.proxies:
            raise Services.NoSuchKey(key)

        print("unlink: {0}".format(key))
        del self.proxies[key]
        
    def list(self):
        return self.proxies
        
    def getValue(self,key):
        return self.proxies[key]
      
