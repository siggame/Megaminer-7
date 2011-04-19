// -*-c++-*-

#ifndef PORT_H
#define PORT_H

#include <iostream>
#include "structures.h"

#include "Mappable.h"

///A generic port
class Port : public Mappable {
  public:
  Port(_Port* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  int x();
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  int y();
  ///The ownder of the port
  int owner();

  // Actions
  ///Creates a Pirate at the calling Port
  int createPirate();
  ///Creates a Ship at the calling Port
  int createShip();

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Port ob);
};

#endif


