//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef STRUCTURES_H
#define STRUCTURES_H

struct Connection;
struct _Mappable;
struct _Unit;
struct _Pirate;
struct _Player;
struct _Port;
struct _Ship;
struct _Tile;
struct _Treasure;


struct _Mappable
{
  Connection* _c;
  int id;
  int x;
  int y;
};
struct _Unit
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
  int health;
  int strength;
  int movesLeft;
  int attacksLeft;
  int gold;
};
struct _Pirate
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
  int health;
  int strength;
  int movesLeft;
  int attacksLeft;
  int gold;
};
struct _Player
{
  Connection* _c;
  int id;
  char* playerName;
  int gold;
  int time;
};
struct _Port
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
};
struct _Ship
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
  int health;
  int strength;
  int movesLeft;
  int attacksLeft;
  int gold;
};
struct _Tile
{
  Connection* _c;
  int id;
  int x;
  int y;
  int type;
};
struct _Treasure
{
  Connection* _c;
  int id;
  int x;
  int y;
  int gold;
};

#endif

