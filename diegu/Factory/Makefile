#!/usr/bin/make -f
# -*- mode:makefile -*-

all: run

run:
	python ControllerFactory.py --Ice.Config=Server1.config 1 &
	gnome-terminal -x python ControllerFactory.py --Ice.Config=Server2.config 2 &
	gnome-terminal -x python ControllerFactory.py --Ice.Config=Server3.config 3
