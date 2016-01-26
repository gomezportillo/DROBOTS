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
from Container import *
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
class PlayerI(drobots.Player):
    def __init__(self,broker,adapter,current=None): 
	print "jugador creado"
	self.id_bot_def=0
	self.id_bot_ata=2
	self.broker=broker
	self.adapter=adapter
        prx_factory= broker.stringToProxy("controllerFactory1:tcp -p 9093")
        prx_container=broker.stringToProxy("container1:tcp -p 9095")
        self.factory = drobots.ControllerFactoryPrx.uncheckedCast(prx_factory)
        self.container = drobots.ContainerPrx.uncheckedCast(prx_container)
        
    def makeController(self,bot,current=None):
        #name_controller=("controller"+str(self.id_bot))
	proxy_controller = self.factory.make(bot)
	if(bot.ice_isA("::drobots::Attacker")):
		self.container.link(self.id_bot_ata,proxy_controller)
		self.id_bot_ata+=1
	else:
		self.container.link(self.id_bot_def,proxy_controller)
		self.id_bot_def+=1
		
	return proxy_controller

    def win(self,current=None): 
	print("Win")
	sys.exit(0)
    def lose(self,current=None):
	print("Lose")
	sys.exit(0)
    def gameAbort(self,current=None):
        print("Game Aborted")
        sys.exit(0)
