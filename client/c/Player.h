// -*-c++-*-

#ifndef PLAYER_H
#define PLAYER_H

#include <iostream>
#include "structures.h"


class Player {
  public:
  void* ptr;
  Player(_Player* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///Player's Name
  char* playerName();
  ///Player's Gold
  int gold();
  ///Time remaining
  int time();

  // Actions

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Player ob);
};

#endif


