#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
import math
Ice.loadSlice('./Container.ice  --all -I .')
import drobots 
#from RobotFactory import RobotFactory
from collections import namedtuple

from Client import *
from Player import *
from Container import *

def main():
	print "Diego Molero Marín"
if __name__ == "__main__":
    main()
sys.exit(Client().main(sys.argv))












