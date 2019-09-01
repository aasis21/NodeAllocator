CC=mpicc
SRC:=${wildcard */*.c}
BINS:=${SRC:%.c=%.out}
all: ${BINS}

%.out:	%.c
		${CC} $< -o $@
clean:
		rm -f *.tmp
		rm -rf __pycache__