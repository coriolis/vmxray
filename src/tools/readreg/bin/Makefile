# $Id$

################################################################################

TIMELINE=$(BUILD_BIN)/reglookup-timeline
FILES=$(TIMELINE)

all: $(FILES)

$(TIMELINE):
	cp reglookup-timeline $@

install:
	install -m 0755 $(FILES) $(BIN_PREFIX)

clean:
	rm -f *~
