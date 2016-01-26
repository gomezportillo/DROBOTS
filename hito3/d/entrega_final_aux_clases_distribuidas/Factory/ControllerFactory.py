#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
import math
Ice.loadSlice('../Container.ice  --all -I .')
import drobots
from RobotController import *
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
class ControllerFactoryI(drobots.ControllerFactory):
    def make(self,bot,current=None):
	print "LLamada MAKE"
	if (bot.ice_isA("::drobots::Attacker")):
            servant = RobotControllerAttackerI(bot)
            proxy = current.adapter.addWithUUID(servant)
            controller=drobots.RobotControllerAttackerPrx.uncheckedCast(proxy)
        else:
            servant = RobotControllerDefenderI(bot)
            proxy = current.adapter.addWithUUID(servant)
            controller=drobots.RobotControllerDefenderPrx.uncheckedCast(proxy)

        print controller
        return controller

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ControllerFactoryI()

        adapter = broker.createObjectAdapter("ControllerFactoryAdapter")
        proxy = adapter.add(servant,broker.stringToIdentity("controllerFactory1"))

        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0
        
server = Server()
sys.exit(server.main(sys.argv))
