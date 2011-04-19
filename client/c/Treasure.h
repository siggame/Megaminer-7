// -*-c++-*-

#ifndef TREASURE_H
#define TREASURE_H

#include <iostream>
#include "structures.h"

#include "Mappable.h"

///This is the source of your wealth. When dropped on the ground it will build interest baed on its distance to pirates, if dropped on a port it is added to your ooverall wealth
class Treasure : public Mappable {
  public:
  Treasure(_Treasure* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  int x();
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  int y();
  ///The amount of gold currently with this treasure
  int gold();

  // Actions

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Treasure ob);
};

#endif


