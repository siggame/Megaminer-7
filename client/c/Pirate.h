// -*-c++-*-

#ifndef PIRATE_H
#define PIRATE_H

#include <iostream>
#include "structures.h"

#include "Unit.h"
class Unit;

///A basic pirate. These units are bound to land unless aboard a ship. they can pickup and drop treasure as well as build ports and fight other pirates.
class Pirate : public Unit {
  public:
  Pirate(_Pirate* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  int x();
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  int y();
  ///Represents the owner of the unit.
  int owner();
  ///Current ealth of the unit
  int health();
  ///Attacking strength of the unit (Each point of strength deals 1 health of damage)
  int strength();
  ///Displays the remaining moves for this unit this turn
  int movesLeft();
  ///Displays the remaining attacks for this unit this turn
  int attacksLeft();
  ///Amount of gold carried by the unit.
  int gold();

  // Actions
  ///Move the unit to the designated X and Y coordinates if possible
  int move(int x, int y);
  ///Allows a unit to display a message to the screen.
  int talk(char* message);
  ///Attempt to attack the input target if possible
  int attack(Unit& Target);
  ///Allows the pirate to pickup treasure on the ground.
  int pickupTreasure(int amount);
  ///Allows the pirate to drop treasure they are carrying.
  int dropTreasure(int amount);
  ///Pirate builds a port on a land tile with water tile adjacent. Cannot be within three spaces of another port!
  int buildPort();

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Pirate ob);
};

#endif


