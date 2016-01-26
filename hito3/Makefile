#!/usr/bin/make -f
# -*- mode:makefile -*-

.PHONY: all run dumb factory clean

SERVER = drobots3

all: run

run:
	python main.py --Ice.Config=Locator.config $(SERVER)

dumb:
	python dumb_main.py --Ice.Config=Locator.config $(SERVER)

factory:
	python ServerFactory.py --Ice.Config=ServerFactory.config

clean:
	rm *.pyc *~
