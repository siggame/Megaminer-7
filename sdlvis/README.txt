You'll need SDL, SDL_Image, and SDL_TTF to compile it. All are
portable and pretty small.

Assuming you're on Ubuntu:

sudo apt-get install libsdl1.2-dev
sudo apt-get install libsdl-image1.2-dev
sudo apt-get install libsdl-ttf2.0-dev

It should build easily with make afterward.

In windows you should be able to drag and drop the gamelog on top of the
visualizer to get it to open that file. In Linux you should run the visualizer
with the path to the gamelog as the first argument. 
