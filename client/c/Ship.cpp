// -*-c++-*-

#include "Ship.h"
#include "game.h"

#include "Unit.h"

Ship::Ship(_Ship* pointer)
{
    ptr = (void*) pointer;
}

int Ship::id()
{
  return ((_Ship*)ptr)->id;
}

int Ship::x()
{
  return ((_Ship*)ptr)->x;
}

int Ship::y()
{
  return ((_Ship*)ptr)->y;
}

int Ship::owner()
{
  return ((_Ship*)ptr)->owner;
}

int Ship::health()
{
  return ((_Ship*)ptr)->health;
}

int Ship::strength()
{
  return ((_Ship*)ptr)->strength;
}

int Ship::movesLeft()
{
  return ((_Ship*)ptr)->movesLeft;
}

int Ship::attacksLeft()
{
  return ((_Ship*)ptr)->attacksLeft;
}

int Ship::gold()
{
  return ((_Ship*)ptr)->gold;
}


int Ship::move(int x, int y)
{
  return shipMove( (_Ship*)ptr, x, y);
}

int Ship::talk(char* message)
{
  return shipTalk( (_Ship*)ptr, message);
}

int Ship::attack(Unit& Target)
{
  return shipAttack( (_Ship*)ptr, (_Unit*) Target.ptr);
}



std::ostream& operator<<(std::ostream& stream,Ship ob)
{
  stream << "id: " << ((_Ship*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Ship*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Ship*)ob.ptr)->y  <<'\n';
  stream << "owner: " << ((_Ship*)ob.ptr)->owner  <<'\n';
  stream << "health: " << ((_Ship*)ob.ptr)->health  <<'\n';
  stream << "strength: " << ((_Ship*)ob.ptr)->strength  <<'\n';
  stream << "movesLeft: " << ((_Ship*)ob.ptr)->movesLeft  <<'\n';
  stream << "attacksLeft: " << ((_Ship*)ob.ptr)->attacksLeft  <<'\n';
  stream << "gold: " << ((_Ship*)ob.ptr)->gold  <<'\n';
  return stream;
}

