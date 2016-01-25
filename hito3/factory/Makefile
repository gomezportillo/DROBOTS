#!/usr/bin/make -f
# -*- mode:makefile -*-

all: server

server:
	python ServerFactory.py --Ice.Config=Server.config

client:
	python Client.py "factory1 -t -e 1.1:tcp -h localhost -p 9090"
