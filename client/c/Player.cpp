// -*-c++-*-

#include "Player.h"
#include "game.h"


Player::Player(_Player* pointer)
{
    ptr = (void*) pointer;
}

int Player::id()
{
  return ((_Player*)ptr)->id;
}

char* Player::playerName()
{
  return ((_Player*)ptr)->playerName;
}

int Player::gold()
{
  return ((_Player*)ptr)->gold;
}

int Player::time()
{
  return ((_Player*)ptr)->time;
}




std::ostream& operator<<(std::ostream& stream,Player ob)
{
  stream << "id: " << ((_Player*)ob.ptr)->id  <<'\n';
  stream << "playerName: " << ((_Player*)ob.ptr)->playerName  <<'\n';
  stream << "gold: " << ((_Player*)ob.ptr)->gold  <<'\n';
  stream << "time: " << ((_Player*)ob.ptr)->time  <<'\n';
  return stream;
}

