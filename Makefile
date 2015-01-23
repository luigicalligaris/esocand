#!/usr/bin/env make -f 

CXX=g++
# # CXX=clang

# CXXFLAGS=-O2 -std=c++11 -fPIC -ggdb -m64 -pipe -Wall -W
CXXFLAGS=-O2 -std=c++11 -fPIC -ggdb -m64 -pipe -Wall

all: esocand libesocand testlibesocand

libesocand: libesocand.cpp libesocand.hpp
	$(CXX) $(CXXFLAGS) --shared -o libesocand.so libesocand.cpp

testlibesocand: libesocand.so testlibesocand.cpp  libesocand.hpp
	$(CXX) $(CXXFLAGS) -o testlibesocand testlibesocand.cpp

# esocand: libesocand
esocand: esocand.cpp
	$(CXX) $(CXXFLAGS) -o esocand esocand.cpp

test: testlibesocand
	./testlibesocand