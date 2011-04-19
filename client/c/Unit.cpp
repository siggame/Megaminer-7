// -*-c++-*-

#include "Unit.h"
#include "game.h"

#include "Unit.h"

Unit::Unit(_Unit* pointer)
{
    ptr = (void*) pointer;
}

int Unit::id()
{
  return ((_Unit*)ptr)->id;
}

int Unit::x()
{
  return ((_Unit*)ptr)->x;
}

int Unit::y()
{
  return ((_Unit*)ptr)->y;
}

int Unit::owner()
{
  return ((_Unit*)ptr)->owner;
}

int Unit::health()
{
  return ((_Unit*)ptr)->health;
}

int Unit::strength()
{
  return ((_Unit*)ptr)->strength;
}

int Unit::movesLeft()
{
  return ((_Unit*)ptr)->movesLeft;
}

int Unit::attacksLeft()
{
  return ((_Unit*)ptr)->attacksLeft;
}

int Unit::gold()
{
  return ((_Unit*)ptr)->gold;
}


int Unit::move(int x, int y)
{
  return unitMove( (_Unit*)ptr, x, y);
}

int Unit::talk(char* message)
{
  return unitTalk( (_Unit*)ptr, message);
}

int Unit::attack(Unit& Target)
{
  return unitAttack( (_Unit*)ptr, (_Unit*) Target.ptr);
}



std::ostream& operator<<(std::ostream& stream,Unit ob)
{
  stream << "id: " << ((_Unit*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Unit*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Unit*)ob.ptr)->y  <<'\n';
  stream << "owner: " << ((_Unit*)ob.ptr)->owner  <<'\n';
  stream << "health: " << ((_Unit*)ob.ptr)->health  <<'\n';
  stream << "strength: " << ((_Unit*)ob.ptr)->strength  <<'\n';
  stream << "movesLeft: " << ((_Unit*)ob.ptr)->movesLeft  <<'\n';
  stream << "attacksLeft: " << ((_Unit*)ob.ptr)->attacksLeft  <<'\n';
  stream << "gold: " << ((_Unit*)ob.ptr)->gold  <<'\n';
  return stream;
}

