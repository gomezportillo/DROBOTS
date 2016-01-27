#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
import math
Ice.loadSlice('../ControllerFactory.ice --all -I .')
import drobots
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
class RobotControllerAttackerI(drobots.RobotController):
    def __init__(self,bot,current=None):
        print "controler creado"
        self._bot=bot
        self._x=0
        self._y=0
    def turn(self,current=None):
        print "siguiente turno"
        self.move()
    def attackPos(self,pos,current=None):
        print "Ataca posicion"
        pass
    def getSelfPos(self,current=None):
    	print (self._container.getValue(0))
        print "siguiente turno"
        pass
    def move(self):
        coordenates=self._bot.location()
	angle=270
	velocity=self.calculateVelocity(coordenates.y,10)
	self._bot.drive(int(angle),int(velocity))
    def calculateVelocity(self,y,position_y):
        if((y < position_y+10) and (y >position_y-10)):
		return 20
	else:		
		return 100
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     
class RobotControllerDefenderI(drobots.RobotController):
    def __init__(self,bot,container,current=None):
        print "controler creado"
        self._container=container
        self._bot=bot
        self._x=0
        self._y=0
    def turn(self,current=None):
    	self.move()
        print "siguiente turno"
        pass
    def receiveAngleScan(self,current=None):
        print "enviando angulo scan"
        pass
    def getSelfPos(self,current=None):
    	pos=self.bot.location()
        print "enviando Posicion"+str()
        pass
    def receivePos(self,pos,current=None):
        print "enviando Posicion"
        pass
    def move(self):
        coordenates=self._bot.location()
	angle=270
	velocity=self.calculateVelocity(coordenates.y,10)
	self._bot.drive(int(angle),int(velocity))
    def calculateVelocity(self,y,position_y):
        if((y < position_y+10) and (y >position_y-10)):
		return 20
	else:		
		return 100
        
