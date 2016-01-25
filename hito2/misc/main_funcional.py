#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('Drobots.ice') #carga e interpreta el sirviente en tiempo de ejecución
import drobots #module drobots
import sys, time, math
from random import randint
from auxiliary_functions import *

class Client(Ice.Application): 
    def run(self, argv):
        #--Creamos las entidades que nos van a permitir manejar objetos distribuidos
        broker = self.communicator() #el broker nos permite instanciar objetos distribuidos remotos
        adapter = broker.createObjectAdapter("GenericAdapter") #el adaptador, que guarda el registro de los objetos que tenemos
        adapter.activate()

        #--Creamos el sirviente, instancia de un objeto distribuido, y lo registramos en el adapter, que devuelve su proxy
        player_servant = PlayerI(broker, adapter)
        proxy_player = adapter.add(player_servant, broker.stringToIdentity("player1")) #componente local q representa a un objeto (posibl.
        print("Proxy player: " +str(proxy_player)) #player1 -t -e 1.1:tcp -h 192.168.1.35 -p  
        player = drobots.PlayerPrx.checkedCast(proxy_player) #crea un objeto distr. a partir de su repr. textual (proxy)       

        #--Obtenemos el objeto game a traves del proxy remoto
        proxy_game = broker.stringToProxy(argv[1]) 
        print("Proxy game: " +str(proxy_game))
        game = drobots.GamePrx.checkedCast(proxy_game)
        if not game:
            raise RuntimeError('Invalid proxy')
        
        #--Intentamos conectarnos al juego
        while True:
            try:
                print "Esperando a más jugadores..."
                game.login(player, 'pedroma' + str(randint(0,9)))
                print "pues estamos dentro primo vavava"
                break
            except drobots.GameInProgress:
                print red_nd_bold + "\nPartida en curso. Esperamos 10 segundos y lo intentamos otra vez" + end_format
                time.sleep(10)
                #sys.exit(0)
            except drobots.InvalidProxy:
                print red_nd_bold + "\nProxy inválido negro" + end_format
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

    def makeController(self, robot, adapter, current=None): 
        print "haciendo controlador..."
        rc_servant = RobotControllerI(robot) #87C0C97C-9DD6-4566-BE81-82A3B6C30F7A -t -e 1.1 @ game-server.GameAdapter
        
        rc_proxy = self.adapter.add(rc_servant, self.broker.stringToIdentity("robotcontroller1"))

        robot_controller = drobots.RobotControllerPrx.uncheckedCast(rc_proxy) 
        
        print "Proxy controller: " +str(robot_controller)+"\n"

        return robot_controller                

    
    def win(self, current=None): 
        print yellow_nd_bold + "Hemos ganado!" + end_format
        current.adapter.getCommunicator().shutdown()
#        sys.exit(1)

    def lose(self, current=None):
        print red_nd_bold + "Pues... hemos perdido, loco" + end_format
        current.adapter.getCommunicator().shutdown()


class RobotControllerI(drobots.RobotController):
    def __init__(self, robot):
        self.robot = robot
        self.first = True
    
    def turn(self, current=None):

        try:
            location = self.robot.location()
            delta_x = 500 - location.x
            delta_y = 500 - location.y
            angle = int(round(calculate_angle(delta_x, delta_y), 0))
            print "x: " + str(location.x) + " y: " + str(location.y) + " α: " + str(angle) +"º"        

            if self.first:            
                self.robot.drive(angle, 100)           
                self.first = False                

            self.robot.cannon(angle, 200)
        except drobots.NoEnoughEnergy:
            pass

    def robotDestroyed(self,current=None):
        print "No te lo vas a creer... pero nos han destruido"



sys.exit(Client().main(sys.argv))




