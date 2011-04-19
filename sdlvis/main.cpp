#include "parser.h"
#include "structures.h"

#include <vector>
#include <iostream>
#include <limits>

#include "gui.h"

using namespace std;

int main(int argc, char** argv)
{
  Game g;
  
  bool arenaMode = false;
  
  if(argc == 2)
  {
    parseFile(g, argv[1]);
  }
  else if(argc == 3 && strcmp(argv[1],"-arena") == 0)
  {
    parseFile(g, argv[2]);
    arenaMode = true;
  }
  else
  {
    parseFile(g, "test.gamelog");
  }
      
  initGUI(arenaMode);
  
  mainLoop(g, arenaMode);
  
  SDL_Quit();
  
  return 0;
}
