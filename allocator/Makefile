CXX = g++
SRC := src/min_diameter.cpp
BINS := minD
INCLUDE := include/
SHARED := lib/libsqlite3.so

FLAGS := -I ${INCLUDE}

all: ${BINS}

minD:	src/min_diameter.cpp
	$(CXX) $< -o $@ ${FLAGS} ${SHARED}

clean: 
	rm minD
