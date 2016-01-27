#!/usr/bin/python
# -*- coding: utf-8 -*-


import Ice
Ice.loadSlice('my_interface.ice --all -I .')
import drobots
import sys

class ContainerI(drobots.Container):
    def __init__(self, current=None):
        self.proxies = dict()

    def link(self, key, proxy, current=None):
        print("{0}: link: {1} -> {2}".format(self.type, key, proxy))
        self.proxies[key] = proxy

    def unlink(self, key, current=None):
        print("{0}: unlink: {1}".format(self.type, key))
        del self.proxies[key]
        
    def list(self,current=None):
        return self.proxies

    def getElementAt(self, key, current=None):
        return self.proxies[key]

    def setType(self, t, current=None):
        self.type = t
        
class ServerContainer(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("ContainerAdapter")
        servant = ContainerI()
        proxy = adapter.add(servant, broker.stringToIdentity("container1"))

        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0
        

container = ServerContainer()
sys.exit(container.main(sys.argv))
