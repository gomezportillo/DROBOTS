#!/usr/bin/make -f
# -*- mode:makefile -*-

.PHONY: all main dumb factory container clean

SERVER = drobots5

all: main

main:
	python main.py --Ice.Config=Locator.config $(SERVER)

dumb:
	python dumb_main.py --Ice.Config=Locator.config $(SERVER)

factory1:
	python ServerFactory.py --Ice.Config=ServerFactory1.config

factory2:
	python ServerFactory.py --Ice.Config=ServerFactory2.config

factory3:
	python ServerFactory.py --Ice.Config=ServerFactory3.config

container:
	python ServerContainer.py --Ice.Config=ServerContainer.config

clean:
	rm *.pyc *~

#everything:
#	gnome-terminal -e make factory --tab -e make container --tab -e make dumb --tab -e make run

