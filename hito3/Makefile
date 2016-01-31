#!/usr/bin/make -f
# -*- mode:makefile -*-

.PHONY: all main dumb-player container clean all-factories everything

SERVER = drobots7

all: everything

main:
	python main.py --Ice.Config=Locator.config $(SERVER)

dumb-player:
	python dumb_main.py --Ice.Config=Locator.config $(SERVER)

factory1:
	python ServerFactory.py --Ice.Config=ServerFactory1.config

factory2:
	python ServerFactory.py --Ice.Config=ServerFactory2.config

factory3:
	python ServerFactory.py --Ice.Config=ServerFactory3.config

factory4:
	python ServerFactory.py --Ice.Config=ServerFactory4.config

container:
	python ServerContainer.py --Ice.Config=ServerContainer.config

clean:
	rm *.pyc *~

all-factories:
	make -j factory1 factory2 factory3 factory4

everything:
	gnome-terminal --tab -e "make all-factories"
	gnome-terminal --tab -e "make container"
	gnome-terminal --tab -e "make dumb-player"
#	make main
	gnome-terminal --tab -e "make main


