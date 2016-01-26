#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Pedro-Manuel Gómez-Portillo López, 3ºA
"""

import Ice
Ice.loadSlice('my_interface.ice --all -I .')
import drobots
import sys, time, random, socket
from auxiliary_functions import *

class Client(Ice.Application): 
    def run(self, argv):

        broker = self.communicator()
        adapter = broker.createObjectAdapter('GenericAdapter')
        adapter.activate()

        player_servant = PlayerI(broker, adapter)
        proxy_player = adapter.add(player_servant, broker.stringToIdentity('player1'))
        print 'Proxy player: ' +str(proxy_player)
        player = drobots.PlayerPrx.checkedCast(proxy_player)

        proxy_game = broker.stringToProxy(argv[1]) 
        print 'Proxy game: ' +str(proxy_game)
        game = drobots.GamePrx.checkedCast(proxy_game)
        if not game:
            raise RuntimeError('Invalid proxy')
        

        while True:
            try:
                print 'Intentando hacer login...'
                game.login(player, 'pdrm' + str(random.randint(0,99)))
                print 'Estamos dentro. Esperando a que nos pidan el robot controller'
                break
            except drobots.GameInProgress:
                print red_nd_bold + "\nPartida en curso. Esperamos 10 segundos y lo intentamos otra vez" + end_format
                time.sleep(10)
            except drobots.InvalidProxy:
                print red_nd_bold + "\nProxy inválido loco" + end_format
                sys.exit(0)
            except drobots.InvalidName, e:
                print red_nd_bold + "\nNombre inválido primo" + end_format
                print str(e.reason)
                sys.exit(0)               

        
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 1

class PlayerI(drobots.Player):
    def __init__(self, broker, adapter):
        self.broker = broker
        self.adapter = adapter    
        self.rc_counter = 0    
        self.factory = self.createControllerFactory()
        self.container = Container()

    def createControllerFactory(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('atclab.esi.uclm.es', 80))
        my_ip = s.getsockname()[0]

        factory_proxy = self.broker.stringToProxy('factory1 -t -e 1.1:tcp -h '+my_ip+' -p 9090 -t 60000')
        factory = drobots.ControllerFactoryPrx.checkedCast(factory_proxy)

        if not factory:
            raise RuntimeError('Invalid factory proxy')
        
        return factory
    
    def makeController(self, robot, current=None): 
        print 'Haciendo robot controller...'
        name = 'rc' + str(self.rc_counter)
        self.rc_counter += 1

        rc_proxy = self.factory.make(robot)
        self.container.link(name, rc_proxy)
        rc = drobots.RobotControllerPrx.uncheckedCast(rc_proxy)
        return rc

    def win(self, current=None): 
        print yellow_nd_bold + "Hemos ganado!" + end_format
        self.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print red_nd_bold + "Pues... hemos perdido, loco" + end_format
        self.adapter.getCommunicator().shutdown()

class Container:
    def __init__(self):
        self.proxies = dict()

    def link(self, key, proxy, current=None):
        try:
            self.proxies[key] = proxy
        except KeyError:
            print "Key "+key+" was not found"

    def unlink(self, key, current=None):
        try:
            del self.proxies[key]
        except KeyError:
            print "Key "+key+" was not found"

    def getProxie(self, key,current=None):
        return self.proxies[key]



sys.exit(Client().main(sys.argv))




