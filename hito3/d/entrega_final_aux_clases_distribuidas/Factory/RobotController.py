#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
import math
Ice.loadSlice('../Container.ice --all -I .')
import drobots
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
class RobotControllerAttackerI(drobots.RobotController):
    def __init__(self,bot,current=None):
        print "controler creado"
        self._bot=bot
    def turn(self,current=None):
        print "siguiente turno"
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     
class RobotControllerDefenderI(drobots.RobotController):
    def __init__(self,bot,current=None):
        print "controler creado"
        self._bot=bot
    def turn(self,current=None):
        print "siguiente turno"


