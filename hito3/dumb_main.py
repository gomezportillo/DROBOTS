#!/usr/bin/python
# -*- coding: utf-8 -*-
import Ice
Ice.loadSlice('my_interface.ice --all -I .')
import drobots
import sys, time, random
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
        self.factory = ControllerFactory(self.broker, self.adapter)

    def makeController(self, robot, adapter, current=None): 
        print 'Haciendo robot controller...'
        name = 'rc' + str(self.rc_counter)
        self.rc_counter += 1

        rc_proxy = self.factory.make(robot, name)
        rc = drobots.RobotControllerPrx.checkedCast(rc_proxy)
        return rc             
    
    def win(self, current=None): 
        print yellow_nd_bold + "Hemos ganado!" + end_format
        self.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print red_nd_bold + "Pues... hemos perdido, loco" + end_format
        self.adapter.getCommunicator().shutdown()

class ControllerFactory:
    def __init__(self,broker, adapter):
        self.broker=broker
        self.adapter=adapter

    def make(self, bot, name, current=None):
        if bot.ice_isA("::drobots::Attacker"):
            rc_servant = RobotControllerAttacker(bot)
        else:
            rc_servant = RobotControllerDefender(bot)
 
        rc_proxy = self.adapter.add(rc_servant, self.broker.stringToIdentity(name))
        return rc_proxy

class RobotControllerI(drobots.RobotController):
    pass

class RobotControllerAttacker(RobotControllerI): 

    def __init__(self, robot):
        self.robot = robot
        self.state = State.MOVING
        self.previous_damage = 0
        self.move_to = Point(10, 10)
        self.shoot_angle = 0
        self.shoots_counter = 0

        self.handlers = {
            State.MOVING : self.move,
            State.SHOOTING : self.shoot,
            State.PLAYING : self.playing
        }
        
    
    def turn(self, current=None):
        try:
            self.handlers[self.state]()
        except drobots.NoEnoughEnergy:
            pass

    def playing(self):
        location = self.robot.location()
        print 'Soy Attacker y estoy en ' + str(location.x) + ', ' + str(location.y)

    def move(self):
        location = self.robot.location()
        delta_x = self.move_to.x - location.x
        delta_y = self.move_to.y - location.y
        angle = int(round(calculate_angle(delta_x, delta_y), 0))
        print 'Moving to x: ' + str(location.x) + ' y: ' + str(location.y) + ' α: ' + str(angle) + 'º'
        self.robot.drive(angle, 100)
        self.state = State.PLAYING

    def shoot(self): 
        MAX_SHOOTS = 30
        if self.shoots_counter <= MAX_SHOOTS:
            angle = self.shoot_angle + random.randint(0, +10)
            distance = (self.shoots_counter + 6) * 20
            self.robot.cannon(angle, distance) 
            print 'Shooting to α: ' + str(angle) + 'º distance: ' + str(distance)
            self.shoots_counter += 1
        else: #lo damos por muerto y pasamos a escanear otros ángulos
            self.shoots_counter = 0
            self.state = State.MOVING 

    def checkPosition(self):      
        location = self.robot.location()
        delta_x = self.move_to.x - location.x
        delta_y = self.move_to.y - location.y
        if abs(delta_x) < 10 or abs(delta_y) < 10:   
            self.move_to = Point(random.randint(0, 999), random.randint(0, 999))
            self.state = State.MOVING
    
    def robotDestroyed(self,current=None):
        print 'No te lo vas a creer... pero nos han destruido uno de los atacantes'


class RobotControllerDefender(RobotControllerI):

    def __init__(self, robot):
        self.robot = robot
        self.state = State.MOVING
        self.previous_damage = 0
        self.move_to = Point(990, 990)
        self.all_angles = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]
        self.angles_left_to_scan = self.all_angles[:]
        random.shuffle(self.angles_left_to_scan)

        self.handlers = {
            State.MOVING : self.move,
            State.SCANNING : self.scan,
            State.PLAYING : self.playing
        }

    def turn(self, current=None):
        try:
            self.handlers[self.state]()
        except drobots.NoEnoughEnergy:
            pass

    def playing(self):
        location = self.robot.location()
        print 'Soy Defender y estoy en '+ str(location.x) + ', ' + str(location.y)

    def move(self):
        location = self.robot.location()
        delta_x = self.move_to.x - location.x
        delta_y = self.move_to.y - location.y
        angle = int(round(calculate_angle(delta_x, delta_y), 0))
        print 'Moving to x: ' + str(location.x) + ' y: ' + str(location.y) + ' α: ' + str(angle) + 'º'
        self.robot.drive(angle, 100)
        self.state = State.PLAYING


    def scan(self): 
        amplitude = 20        
        try:
            current_angle = self.angles_left_to_scan.pop()
        except IndexError:
            self.angles_left_to_scan = self.all_angles[:]
            random.shuffle(self.angles_left_to_scan)
            current_angle = self.angles_left_to_scan.pop()            
            
        detected_enemies = self.robot.scan(current_angle, amplitude)
        if  detected_enemies <> 0:
            self.robot.drive(0, 0) #torreta mode: ON
            self.shoot_angle = current_angle
            self.state = State.SHOOTING
        print 'Scanning to amplitude: ' + str(amplitude) + ' α: ' + str(current_angle) + 'º. Detected enemies: ' + str(detected_enemies)
        self.checkPosition()

    def checkPosition(self):      
        location = self.robot.location()
        delta_x = self.move_to.x - location.x
        delta_y = self.move_to.y - location.y
        if abs(delta_x) < 10 or abs(delta_y) < 10:   
            self.move_to = Point(random.randint(0, 999), random.randint(0, 999))
            self.state = State.MOVING
    
    def robotDestroyed(self,current=None):
        print 'No te lo vas a creer... pero nos han destruido uno de los defensores'


sys.exit(Client().main(sys.argv))
