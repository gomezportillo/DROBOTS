#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
import math
Ice.loadSlice('./ControllerFactory.ice  --all -I .')
import drobots 
#from RobotFactory import RobotFactory
from collections import namedtuple

from Client import *

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
class PlayerI(drobots.Player):
    def __init__(self,broker,adapter,current=None): 
	print "jugador creado"
	self.counter=0
	self.broker=broker
	self.adapter=adapter
	self.factories= dict()
        prx_factory1 = broker.stringToProxy("controllerFactory1:tcp -h 172.19.220.5 -p 9074")
        prx_factory2 = broker.stringToProxy("controllerFactory2:tcp -h 172.19.220.5 -p 9082")
        prx_factory3 = broker.stringToProxy("controllerFactory3:tcp -h 172.19.220.5 -p 9083")
        prx_container=broker.stringToProxy("container1:tcp -h 172.19.220.5 -p 9096")
        self.factories[0] = drobots.ControllerFactoryPrx.uncheckedCast(prx_factory1)
        self.factories[1] = drobots.ControllerFactoryPrx.uncheckedCast(prx_factory2)
        self.factories[2] = drobots.ControllerFactoryPrx.uncheckedCast(prx_factory3)
        self.container = drobots.ContainerPrx.uncheckedCast(prx_container)
        
    def makeController(self,bot,current=None):
    	print("Llamada make")
    	id_factory=self.counter%3
    	print ("Id factory:"+str(id_factory))
	controller = self.factories[id_factory].make(bot,self.container)
	self.counter+=1
	return controller

    def win(self,current=None): 
	print("Win")
	sys.exit(0)
    def lose(self,current=None):
	print("Lose")
	sys.exit(0)
    def gameAbort(self,current=None):
        print("Game Aborted")
        sys.exit(0)
