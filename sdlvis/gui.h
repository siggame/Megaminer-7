#include <SDL.h>

#include "structures.h"

bool initGUI(bool arenaMode);

void renderMap(Game& g);

void renderTurn(Game& g, int turn, int xTile, int yTile);

void mainLoop(Game& g, bool arenaMode);

void handleMouse(int & turn, int x, int y, Game& g);

