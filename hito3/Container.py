#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('my_interface.ice --all -I .')
import drobots
import sys

class ContainerI(drobots.Container):
    def __init__(self,current=None):
        self.proxies = dict()

    def link(self, key, proxy, current=None):
        print("link: {0} -> {1}".format(key, proxy))
        self.proxies[key] = proxy

    def unlink(self, key, current=None):
        print("unlink: {0}".format(key))
        del self.proxies[key]
        
    def list(self,current=None):
        return self.proxies
