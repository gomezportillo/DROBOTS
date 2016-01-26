#!/usr/bin/python
# -*- coding: utf-8 -*-


import Ice
Ice.loadSlice('my_interface.ice --all -I .')
import drobots
import sys

class ContainerI(drobots.Container):
    def __init__(self,current=None):
        self.proxies = dict()

    def link(self, key, proxy,current=None):
        if key in self.proxies:
            raise Services.AlreadyExists(key)

        print("link: {0} -> {1}".format(key, proxy))
        self.proxies[key] = proxy

    def unlink(self, key,current=None):
        if not key in self.proxies:
            raise Services.NoSuchKey(key)

        print("unlink: {0}".format(key))
        del self.proxies[key]
        
    def list(self,current=None):
        return self.proxies
        
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
