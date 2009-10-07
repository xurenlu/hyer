all:tidylib.so
tidylib.so: access.o alloc.o attrask.o attrdict.o attrget.o attrs.o buffio.o clean.o config.o entities.o fileio.o istack.o lexer.o localize.o parser.o pprint.o streamio.o tagask.o tags.o tidylib.o tmbstr.o utf8.o 
	gcc -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions  tidylib/src/access.o tidylib/src/alloc.o tidylib/src/attrask.o tidylib/src/attrdict.o tidylib/src/attrget.o tidylib/src/attrs.o tidylib/src/buffio.o tidylib/src/clean.o tidylib/src/config.o tidylib/src/entities.o tidylib/src/fileio.o tidylib/src/istack.o tidylib/src/lexer.o tidylib/src/localize.o tidylib/src/parser.o tidylib/src/pprint.o tidylib/src/streamio.o tidylib/src/tagask.o tidylib/src/tags.o tidylib/src/tidylib.o tidylib/src/tmbstr.o tidylib/src/utf8.o -o tidylib/lib/tidylib.so
access.o:tidylib/src/access.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/access.c -o tidylib/src/access.o
alloc.o:tidylib/src/alloc.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/alloc.c -o tidylib/src/alloc.o
attrask.o:tidylib/src/attrask.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/attrask.c -o tidylib/src/attrask.o
attrdict.o:tidylib/src/attrdict.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/attrdict.c -o tidylib/src/attrdict.o
attrget.o:tidylib/src/attrget.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/attrget.c -o tidylib/src/attrget.o
attrs.o:tidylib/src/attrs.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/attrs.c -o tidylib/src/attrs.o
buffio.o:tidylib/src/buffio.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/buffio.c -o tidylib/src/buffio.o
clean.o:tidylib/src/clean.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/clean.c -o tidylib/src/clean.o
config.o:tidylib/src/config.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/config.c -o tidylib/src/config.o
entities.o:tidylib/src/entities.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/entities.c -o tidylib/src/entities.o
fileio.o:tidylib/src/fileio.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/fileio.c -o tidylib/src/fileio.o
istack.o:tidylib/src/istack.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/istack.c -o tidylib/src/istack.o
lexer.o:tidylib/src/lexer.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/lexer.c -o tidylib/src/lexer.o
localize.o:tidylib/src/localize.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/localize.c -o tidylib/src/localize.o
parser.o:tidylib/src/parser.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/parser.c -o tidylib/src/parser.o
pprint.o:tidylib/src/pprint.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/pprint.c -o tidylib/src/pprint.o
streamio.o:tidylib/src/streamio.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/streamio.c -o tidylib/src/streamio.o
tagask.o:tidylib/src/tidylib.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/tagask.c -o tidylib/src/tagask.o
tags.o:tidylib/src/tags.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/tags.c -o tidylib/src/tags.o
tidylib.o:tidylib/src/tidylib.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/tidylib.c -o tidylib/src/tidylib.o
tmbstr.o:tidylib/src/tmbstr.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/tmbstr.c -o tidylib/src/tmbstr.o
utf8.o:tidylib/src/utf8.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DNDEBUG -Itidylib/include -I/usr/include/python2.6 -c tidylib/src/utf8.c -o tidylib/src/utf8.o

