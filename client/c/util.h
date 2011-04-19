#ifndef UTIL_H
#define UTIL_H

#include "structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)
#else
#define DLLEXPORT
#endif



#ifdef __cplusplus
extern "C"
{
#endif
  //pathfinding

  DLLEXPORT int getPathSize();
  DLLEXPORT int getPathStep(int i);
  DLLEXPORT int findPath(_Tile* start, _Tile* end, int type);
  
#ifdef __cplusplus
}
#endif

#endif

