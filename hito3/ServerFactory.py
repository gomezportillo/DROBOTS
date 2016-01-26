#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('my_interface.ice --all -I .')
import drobots, sys
from RobotControllers import *

class ControllerFactoryI(drobots.ControllerFactory):
    def __init__(self):
        self.key = 0

    def make(self, robot, container, current=None):
        print "Factoria llamada"        

        if robot.ice_isA("::drobots::Attacker"):
            rc_servant = RobotControllerAttackerI(robot, container)
            rc_proxy = current.adapter.addWithUUID(rc_servant)
            container.link(self.key, rc_proxy)
            rc = drobots.RobotControllerAttackerPrx.uncheckedCast(rc_proxy)

        else:
            rc_servant = RobotControllerDefenderI(robot, container)
            rc_proxy = current.adapter.addWithUUID(rc_servant)
            container.link(self.key, rc_proxy)
            rc = drobots.RobotControllerDefenderPrx.uncheckedCast(rc_proxy)

        self.key += 1
        return rc

class ServerFactory(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("FactoryAdapter")
        servant = ControllerFactoryI()
        proxy = adapter.add(servant, broker.stringToIdentity("factory1"))
        
        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


factory = ServerFactory()
sys.exit(factory.main(sys.argv))
