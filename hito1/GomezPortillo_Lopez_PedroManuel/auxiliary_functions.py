#!/usr/bin/env python

import math

bold = '\033[1m'
red_nd_bold = '\033[91m' + bold                 #for printing errors
yellow_nd_bold = '\033[93m' + '\033[4m' + bold  #for printing a winning result
end_format = '\033[0m'                          #for ending the format


def calculate_angle(x, y):
	if x==0:
		if y>0:
			return 90
		return 270
	if y==0:
		if x>0:
			return 0
		return 180
	elif y>0:
		return 90 - math.degrees(math.atan(float(x)/float(y)))
	else:
		return 270 - math.degrees(math.atan(float(x)/float(y)))
