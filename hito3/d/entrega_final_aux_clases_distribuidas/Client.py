#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
import math
Ice.loadSlice('./Container.ice --all -I .')
import drobots 
#from RobotFactory import RobotFactory
from collections import namedtuple

from Player import *
from Container import *
class Client(Ice.Application): 
    def run(self, argv):
	broker = self.communicator()
	######################################################
	adapter = broker.createObjectAdapter("Adapter")
	servant = PlayerI(broker,adapter)
	proxy_player = adapter.add(servant, broker.stringToIdentity("player1"))
	print(proxy_player)
	adapter.activate()
	sys.stdout.flush()
	######################################################
	player = drobots.PlayerPrx.checkedCast(proxy_player)
	adapter.activate() #activar el adaptador
	######################################################
        proxy_game = self.communicator().stringToProxy(argv[1])
	print(proxy_game)
        game = drobots.GamePrx.checkedCast(proxy_game)
        if not game:
            raise RuntimeError('Invalid proxy')
	######################################################
	game.login(player,"Diego2");
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0
