CXX = g++
SRC:=${wildcard */*.cpp}
BINS:=${SRC:%.cpp=%.out}
INCLUDE := include/
SHARED := lib/libsqlite3.so

FLAGS := -I ${INCLUDE}

all: ${BINS}

%.out:	%.cpp
	$(CXX) $< -o $@ ${FLAGS} ${SHARED}

clean: 
	rm minD
