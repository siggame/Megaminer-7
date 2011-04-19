// -*-c++-*-

#include "Treasure.h"
#include "game.h"


Treasure::Treasure(_Treasure* pointer)
{
    ptr = (void*) pointer;
}

int Treasure::id()
{
  return ((_Treasure*)ptr)->id;
}

int Treasure::x()
{
  return ((_Treasure*)ptr)->x;
}

int Treasure::y()
{
  return ((_Treasure*)ptr)->y;
}

int Treasure::gold()
{
  return ((_Treasure*)ptr)->gold;
}




std::ostream& operator<<(std::ostream& stream,Treasure ob)
{
  stream << "id: " << ((_Treasure*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Treasure*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Treasure*)ob.ptr)->y  <<'\n';
  stream << "gold: " << ((_Treasure*)ob.ptr)->gold  <<'\n';
  return stream;
}

