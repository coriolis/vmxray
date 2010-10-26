# $Id$

################################################################################

REGLOOKUP=$(BUILD_BIN)/reglookup
OBJ=$(wildcard ../lib/*.o)
FILES=$(REGLOOKUP)

all: $(FILES)

$(REGLOOKUP): reglookup.o $(OBJ)
	$(CC) $(CFLAGS) $(OPTS) $(LIB) -o $@ reglookup.o $(OBJ)

reglookup.o: reglookup.c
	$(CC) $(CFLAGS) $(OPTS) $(INC) -c -o $@ reglookup.c

install:
	install -m 0755 $(FILES) $(BIN_PREFIX)

clean:
	rm -f *.o
