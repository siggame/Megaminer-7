// -*-c++-*-

#include "Port.h"
#include "game.h"


Port::Port(_Port* pointer)
{
    ptr = (void*) pointer;
}

int Port::id()
{
  return ((_Port*)ptr)->id;
}

int Port::x()
{
  return ((_Port*)ptr)->x;
}

int Port::y()
{
  return ((_Port*)ptr)->y;
}

int Port::owner()
{
  return ((_Port*)ptr)->owner;
}


int Port::createPirate()
{
  return portCreatePirate( (_Port*)ptr);
}

int Port::createShip()
{
  return portCreateShip( (_Port*)ptr);
}



std::ostream& operator<<(std::ostream& stream,Port ob)
{
  stream << "id: " << ((_Port*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Port*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Port*)ob.ptr)->y  <<'\n';
  stream << "owner: " << ((_Port*)ob.ptr)->owner  <<'\n';
  return stream;
}

