# $Id$

BUILD_FILES=$(BUILD_DOC)/man/man1/reglookup.1.gz $(BUILD_DOC)/man/man1/reglookup-timeline.1.gz

all: 

	docbook2x-man --to-stdout reglookup.1.docbook > man/man1/reglookup.1
	docbook2x-man --to-stdout reglookup-timeline.1.docbook > man/man1/reglookup-timeline.1
	cd man/man1 && gzip -9 -f reglookup.1
	cd man/man1 && gzip -9 -f reglookup-timeline.1
