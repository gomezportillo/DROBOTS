#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('my_interface.ice --all -I .')
import drobots, sys
from RobotControllers import *

class ControllerFactoryI(drobots.ControllerFactory):
    def __init__(self):
        self.key = 0

    def make(self, robot, container_robots, current=None):
        print "make de factoria llamadao"        

        if robot.ice_isA("::drobots::Attacker"):
            rc_servant = RobotControllerAttackerI(robot)
            rc_proxy = current.adapter.addWithUUID(rc_servant)
            print rc_proxy                  
            container_robots.link(self.key, rc_proxy)
            self.key += 1
            rc = drobots.RobotControllerAttackerPrx.uncheckedCast(rc_proxy)
            rc.setContainer(container_robots)

        else:
            rc_servant = RobotControllerDefenderI(robot, container_robots)
            rc_proxy = current.adapter.addWithUUID(rc_servant)
            print rc_proxy                  
            container_robots.link(self.key, rc_proxy)
            self.key += 1
            rc = drobots.RobotControllerDefenderPrx.uncheckedCast(rc_proxy)
            rc.setContainer(container_robots)

        return rc

class ServerFactory(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("FactoryAdapter")
        servant = ControllerFactoryI()
        proxy = adapter.add(servant, broker.stringToIdentity("factory"))        

        print(proxy) #'factory1 -t -e 1.1:tcp -h ' +my ip +' -p 9091 -t 60000'

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


factory = ServerFactory()
sys.exit(factory.main(sys.argv))
