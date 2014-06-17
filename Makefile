#!/usr/bin/env make -f 

all: esocand.cpp
	g++ -O2 -std=c++11 -o esocand esocand.cpp