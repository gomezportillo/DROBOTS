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
        self.counter = 0
        self.my_ip = self.get_my_IP()
        self.container_factories = self.create_container_of_factories() #filled up of factories!
        self.container_robots = self.create_container_of_robots()

    def get_my_IP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('atclab.esi.uclm.es', 80))
        my_ip = s.getsockname()[0]
        return my_ip

    def create_container_of_factories(self):
        string_prx = 'container1 -t -e 1.1:tcp -h '+self.my_ip+' -p 9190 -t 60000'
        container_proxy = self.broker.stringToProxy(string_prx)
        factories_container = drobots.ContainerPrx.checkedCast(container_proxy)
        factories_container.setType("ContainerF")

        for i in range(0,4):
            string_prx = 'factory -t -e 1.1:tcp -h '+self.my_ip+' -p 909'+str(i)+' -t 60000'
            factory_proxy = self.broker.stringToProxy(string_prx)
            print factory_proxy
            factory = drobots.ControllerFactoryPrx.checkedCast(factory_proxy)
            
            if not  factory:
                raise RuntimeError('Invalid factory '+i+' proxy')
        
            factories_container.link(i, factory_proxy)
        
        return factories_container

    def create_container_of_robots(self):
        container_proxy = self.broker.stringToProxy('container1 -t -e 1.1:tcp -h '+self.my_ip+' -p 9190 -t 60000')
        controller_container = drobots.ContainerPrx.checkedCast(container_proxy)
        controller_container.setType("ContainerC")

        if not controller_container:
            raise RuntimeError('Invalid factory proxy')
        
        return controller_container


    def makeController(self, robot, current=None):
        i = self.counter % 4
        self.counter += 1
        print 'Haciendo robot controller en factoría ' + str(i)
        factory_proxy = self.container_factories.getElementAt(i)
        print factory_proxy
        factory = drobots.ControllerFactoryPrx.checkedCast(factory_proxy)
        rc = factory.make(robot, self.container_robots)
        return rc

    def win(self, current=None): 
        print yellow_nd_bold + "Hemos ganado!" + end_format
        self.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print red_nd_bold + "Pues... hemos perdido, loco" + end_format
        self.adapter.getCommunicator().shutdown()


sys.exit(Client().main(sys.argv))

