all: tidylib2.so
	gcc -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions  access.o alloc.o attrask.o attrdict.o attrget.o attrs.o buffio.o clean.o config.o entities.o fileio.o istack.o lexer.o localize.o parser.o pprint.o streamio.o tagask.o tags.o tidylib.o tmbstr.o utf8.o  -o tidylib2.so
tidylib2.so: access.o alloc.o attrask.o attrdict.o attrget.o attrs.o buffio.o clean.o config.o entities.o fileio.o istack.o lexer.o localize.o parser.o pprint.o streamio.o tagask.o tags.o tidylib.o tmbstr.o utf8.o 
gon:
	#gcc -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions  access.o alloc.o attrask.o attrdict.o attrget.o attrs.o buffio.o clean.o config.o entities.o fileio.o istack.o lexer.o localize.o parser.o pprint.o streamio.o tagask.o tags.o tidylib.o tmbstr.o utf8.o  -o tidylib2.so
access.o: access.c

js:
	rm dump
	gcc -pthread  -Wl,-O1 -Wl,-Bsymbolic-functions  access.o alloc.o attrask.o attrdict.o attrget.o attrs.o buffio.o clean.o config.o entities.o fileio.o istack.o lexer.o localize.o parser.o pprint.o streamio.o tagask.o tags.o tidylib.o tmbstr.o utf8.o dump.o -o  dump
	./dump
en:
	LC_ALL=en_US.UTF-8 gcc dump.c -ltidy -I/usr/include/tidy -o dump

ci:
	LC_ALL=en_US.UTF-8 gcc dump.c -ltidy -I/usr/include/tidy -o dump -E
bak:
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes  -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c dump.c -o dump
so:
	rm *.so
	gcc -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions  access.o alloc.o attrask.o attrdict.o attrget.o attrs.o buffio.o clean.o config.o entities.o fileio.o istack.o lexer.o localize.o parser.o pprint.o streamio.o tagask.o tags.o tidylib.o tmbstr.o utf8.o  -o tidylib2.so

#gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes  -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c dump.c -o dump.o

