#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
import math
Ice.loadSlice('../ControllerFactory.ice --all -I .')
import drobots 

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#Guarda proxies de controler, no de robots
class ContainerI(drobots.Container):
    def __init__(self,current=None):
        self.proxies = dict()
        self.counter = 0
    def link(self, key, proxy,current=None):
        if key in self.proxies:
            raise Services.AlreadyExists(key)

        print("link: {0} -> {1}".format(key, proxy))
        self.proxies[key] = proxy
        
    def linkRB(self, proxy,current=None):
        if self.counter in self.proxies:
            raise Services.AlreadyExists(self.counter)

        print("link: {0} -> {1}".format(self.counter, proxy))
        self.proxies[self.counter] = proxy
        self.counter+=1

    def unlink(self, key,current=None):
        if not key in self.proxies:
            raise Services.NoSuchKey(key)

        print("unlink: {0}".format(key))
        del self.proxies[key]
        
    def list(self,current=None):
        return self.proxies
        
    def getValue(self,key,current=None):
        return self.proxies[key]


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ContainerI()

        adapter = broker.createObjectAdapter("ContainerAdapter")
        proxy = adapter.add(servant,broker.stringToIdentity("container1"))

        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0
        
server = Server()
sys.exit(server.main(sys.argv))
