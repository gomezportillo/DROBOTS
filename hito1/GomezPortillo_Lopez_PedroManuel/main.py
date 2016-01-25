#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('Drobots.ice')
import drobots
import sys, time, math
from auxiliary_functions import *

class Client(Ice.Application): 
    def run(self, argv):

        broker = self.communicator() 
        adapter = broker.createObjectAdapter("GenericAdapter") 
        adapter.activate()

        player_servant = PlayerI(broker, adapter)
        proxy_player = adapter.add(player_servant, broker.stringToIdentity("player1")) 
        print("Proxy player: " +str(proxy_player))
        player = drobots.PlayerPrx.checkedCast(proxy_player) 

        proxy_game = broker.stringToProxy(argv[1]) 
        print("Proxy game: " +str(proxy_game))
        game = drobots.GamePrx.checkedCast(proxy_game)
        if not game:
            raise RuntimeError('Invalid proxy')
        
        while True:
            try:
                game.attach(player)
                break
            except drobots.GameInProgress:
                print red_nd_bold + "\nPartida en curso. Esperamos 10 segundos y lo intentamos otra vez" + end_format
                time.sleep(10)
                #sys.exit(0)
        
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 1

class PlayerI(drobots.Player):
    def __init__(self, broker, adapter):
        self.broker = broker
        self.adapter = adapter        

    def makeController(self, robot, adapter, current=None): 
        rc_servant = RobotControllerI(robot)
        
        rc_proxy = self.adapter.add(rc_servant, self.broker.stringToIdentity("robotcontroller1"))

        robot_controller = drobots.RobotControllerPrx.uncheckedCast(rc_proxy) 
        
        print("Proxy controller: " +str(robot_controller)+"\n")

        return robot_controller                

    
    def win(self, current=None): 
        print yellow_nd_bold + "Hemos ganado!" + end_format
        sys.exit(1) 

    def lose(self, current=None):
	    print "Pues... hemos perdido"


class RobotControllerI(drobots.RobotController):
    def __init__(self, robot):
        self.robot = robot

    def turn(self, current=None):
        location = self.robot.location()
        delta_x = 500 - location.x
        delta_y = 500 - location.y
        angle = int(round(calculate_angle(delta_x, delta_y), 0))

        velocity = 100
        if abs(delta_x) < 15 or abs(delta_y) < 15: 
            velocity = 1
        
        print "x: " + str(location.x) + " y: " + str(location.y) + " vel: "+ str(velocity) + "u/s α: " + str(angle) +"º"
    
        self.robot.drive(angle, 100)           

    def robotDestroyed(self,current=None):
        print "No te lo vas a creer... pero nos han destruido"



sys.exit(Client().main(sys.argv))




