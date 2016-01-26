#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('my_interface.ice --all -I .')
import drobots
import random
from auxiliary_functions import *

class RobotControllerI(drobots.RobotController):
    pass

class RobotControllerAttackerI(drobots.RobotControllerAttacker): 

    def __init__(self, robot, container):
        self.robot = robot
        self.container = container
        self.state = State.MOVING
        self.previous_damage = 0
        self.move_to = Point(10, 10)
        self.shoot_angle = 0
        self.shoots_counter = 0

        self.handlers = {
            State.MOVING : self.move,
            State.SHOOTING : self.shoot,
            State.PASSING : self.passing
        }
        
    
    def turn(self, current=None):
        try:
            self.handlers[self.state]()
        except drobots.NoEnoughEnergy:
            pass

    def passing(self):
        location = self.robot.location()
        print 'Soy Attacker y estoy en ' + str(location.x) + ', ' + str(location.y)

    def move(self):
        location = self.robot.location()
        delta_x = self.move_to.x - location.x
        delta_y = self.move_to.y - location.y
        angle = int(round(calculate_angle(delta_x, delta_y), 0))
        print 'Moving to x: ' + str(location.x) + ' y: ' + str(location.y) + ' α: ' + str(angle) + 'º'
        self.robot.drive(angle, 100)
        self.state = State.PASSING

    def shoot(self): 
        MAX_SHOOTS = 30
        if self.shoots_counter <= MAX_SHOOTS:
            angle = self.shoot_angle + random.randint(0, +10)
            distance = (self.shoots_counter + 6) * 20
            self.robot.cannon(angle, distance) 
            print 'Shooting to α: ' + str(angle) + 'º distance: ' + str(distance)
            self.shoots_counter += 1
        else: #lo damos por muerto y pasamos a movernos
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


class RobotControllerDefenderI(drobots.RobotControllerDefender):

    def __init__(self, robot, container):
        self.robot = robot
        self.container = container
        self.state = State.MOVING
        self.previous_damage = 0
        self.move_to = Point(990, 990)
        self.all_angles = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]
        self.angles_left_to_scan = self.all_angles[:]
        random.shuffle(self.angles_left_to_scan)

        self.handlers = {
            State.MOVING : self.move,
            State.SCANNING : self.scan,
            State.PASSING : self.passing
        }

    def turn(self, current=None):
        try:
            self.handlers[self.state]()
        except drobots.NoEnoughEnergy:
            pass

    def passing(self):
        location = self.robot.location()
        print 'Soy Defender y estoy en '+ str(location.x) + ', ' + str(location.y)

    def move(self):
        location = self.robot.location()
        delta_x = self.move_to.x - location.x
        delta_y = self.move_to.y - location.y
        angle = int(round(calculate_angle(delta_x, delta_y), 0))
        print 'Moving to x: ' + str(location.x) + ' y: ' + str(location.y) + ' α: ' + str(angle) + 'º'
        self.robot.drive(angle, 100)
        self.state = State.PASSING


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


