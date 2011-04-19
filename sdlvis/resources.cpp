#include "resources.h"

#include "SDL_image.h"

#include <map>
#include <string>
#include <iostream>

using namespace std;

static map<string, SDL_Surface*> images;

SDL_Surface* loadImage(const char* file)
{
  string str = file;
  
  if(images.find(str) != images.end())
    return images.find(str)->second;
  
  SDL_Surface* image = IMG_Load(file);
  if(!image)
  {
    cerr << "IMG_Load: " << IMG_GetError() << endl;
    return NULL;
  }
  
  images[str] = image;
  return image;
  
}