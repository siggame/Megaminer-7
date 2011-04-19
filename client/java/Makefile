JAVAFILES=$(shell ls *.java 2> /dev/null)

all: libclient.so Main.class

submit: Main.class
	@echo "$(shell cd ..;sh submit.sh c)"


libclient.so: ../c/*.cpp ../c/*.h
	$(MAKE) -C ../c/ libclient.so
	cp -f ../c/libclient.so libclient.so

Main.class: $(JAVAFILES) libclient.so
	javac -cp jna.jar:. $(JAVAFILES)

clean:
	rm -f *.class
	rm -f libclient.so
