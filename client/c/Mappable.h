// -*-c++-*-

#ifndef MAPPABLE_H
#define MAPPABLE_H

#include <iostream>
#include "structures.h"


///An object that exists on the grid
class Mappable {
  public:
  void* ptr;
  Mappable(_Mappable* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  int x();
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  int y();

  // Actions

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Mappable ob);
};

#endif


