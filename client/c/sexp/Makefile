sources = lex.yy.cpp $(wildcard *.cpp)
objects = $(sources:%.cpp=%.o)
libclient_objects = $(sources:%.cpp=libclient_%.o)

CFLAGS = -g
CXXFLAGS= -g

all: sexp.a libclient_sexp.a

clean:
	rm -f $(objects) $(libclient_objects) $(deps) sexp.a libclient_sexp.a


%.o: %.cpp
	$(CC) $(CFLAGS) $(CPPFLAGS) -c -o $@ $<

libclient_%.o: override CFLAGS += -fPIC
libclient_%.o: %.cpp
	$(CC) $(CFLAGS) $(CPPFLAGS) -c -o $@ $<

.PHONY: clean all

libclient_sexp.a: ${libclient_objects}
	ar cr $@ $^
	ranlib $@

sexp.a: ${objects}
	ar cr $@ $^
	ranlib $@

