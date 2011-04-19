// -*-c++-*-

#include "Mappable.h"
#include "game.h"


Mappable::Mappable(_Mappable* pointer)
{
    ptr = (void*) pointer;
}

int Mappable::id()
{
  return ((_Mappable*)ptr)->id;
}

int Mappable::x()
{
  return ((_Mappable*)ptr)->x;
}

int Mappable::y()
{
  return ((_Mappable*)ptr)->y;
}




std::ostream& operator<<(std::ostream& stream,Mappable ob)
{
  stream << "id: " << ((_Mappable*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Mappable*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Mappable*)ob.ptr)->y  <<'\n';
  return stream;
}

