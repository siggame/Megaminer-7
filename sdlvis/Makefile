sources = $(wildcard *.cpp)
objects = $(sources:%.cpp=%.o)
CFLAGS += -g `sdl-config  --cflags`
CXXFLAGS += -g `sdl-config  --cflags`
LDFLAGS += `sdl-config  --libs` -lSDL_image -lSDL_ttf

ifeq ($(TARGET), mingw)
CXX:=i586-mingw32-g++
CC:=i586-mingw32-gcc
endif

all: $(objects) sexp/libclient_sexp.a visualizer

clean:
	rm -f $(objects) visualizer
	$(MAKE) -C sexp clean

visualizer: $(objects) sexp/sexp.a
	$(CXX) $(LDFLAGS) $(LOADLIBES) $(LDLIBS) $^ -g -o visualizer

sexp/sexp.a sexp/libclient_sexp.a:
	$(MAKE) -C $(dir $@) $(notdir $@)
