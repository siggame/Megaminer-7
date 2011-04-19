CSFILES=$(shell ls *.CS 2> /dev/null)

all: libclient.so client.exe

submit: Main.class
	@echo "$(shell cd ..;sh submit.sh c)"


libclient.so: ../c/*.cpp ../c/*.h
	$(MAKE) -C ../c/ libclient.so
	cp -f ../c/libclient.so libclient.so

client.exe: $(CSFILES) libclient.so
	mcs -out:client.exe  $(CSFILES)

clean:
	rm -f client.exe
	rm -f libclient.so
