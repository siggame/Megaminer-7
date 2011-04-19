//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef GAME_H
#define GAME_H

#include "network.h"
#include "structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)

#ifdef ENABLE_THREADS
#include "pthread.h"
#endif

#else
#define DLLEXPORT

#ifdef ENABLE_THREADS
#include <pthread.h>
#endif

#endif

struct Connection
{
  int socket;
  
  #ifdef ENABLE_THREADS
  pthread_mutex_t mutex;
  #endif
  
  int turnNumber;
  int playerID;
  int gameNumber;
  int pirateCost;
  int shipCost;
  int portCost;
  int mapSize;

  _Pirate* Pirates;
  int PirateCount;
  _Player* Players;
  int PlayerCount;
  _Port* Ports;
  int PortCount;
  _Ship* Ships;
  int ShipCount;
  _Tile* Tiles;
  int TileCount;
  _Treasure* Treasures;
  int TreasureCount;
};

#ifdef __cplusplus
extern "C"
{
#endif
  DLLEXPORT Connection* createConnection();
  DLLEXPORT void destroyConnection(Connection* c);
  DLLEXPORT int serverConnect(Connection* c, const char* host, const char* port);

  DLLEXPORT int serverLogin(Connection* c, const char* username, const char* password);
  DLLEXPORT int createGame(Connection* c);
  DLLEXPORT int joinGame(Connection* c, int id);

  DLLEXPORT void endTurn(Connection* c);
  DLLEXPORT void getStatus(Connection* c);


//commands

  ///Move the unit to the designated X and Y coordinates
  DLLEXPORT int unitMove(_Unit* object, int x, int y);
  ///Allows a unit to display a message to the screen.
  DLLEXPORT int unitTalk(_Unit* object, char* message);
  ///Attempt to attack the given unit
  DLLEXPORT int unitAttack(_Unit* object, _Unit* Target);
  ///Move the unit to the designated X and Y coordinates
  DLLEXPORT int pirateMove(_Pirate* object, int x, int y);
  ///Allows a unit to display a message to the screen.
  DLLEXPORT int pirateTalk(_Pirate* object, char* message);
  ///Attempt to attack the given unit
  DLLEXPORT int pirateAttack(_Pirate* object, _Unit* Target);
  ///Allows the pirate to pickup treasure on the ground.
  DLLEXPORT int piratePickupTreasure(_Pirate* object, int amount);
  ///Allows the pirate to drop treasure on the groud.
  DLLEXPORT int pirateDropTreasure(_Pirate* object, int amount);
  ///Pirate builds a port on a land tile with water tile adjacent
  DLLEXPORT int pirateBuildPort(_Pirate* object);
  ///Creates a Pirate at the calling Port
  DLLEXPORT int portCreatePirate(_Port* object);
  ///Creates a Ship at the calling Port
  DLLEXPORT int portCreateShip(_Port* object);
  ///Move the unit to the designated X and Y coordinates
  DLLEXPORT int shipMove(_Ship* object, int x, int y);
  ///Allows a unit to display a message to the screen.
  DLLEXPORT int shipTalk(_Ship* object, char* message);
  ///Attempt to attack the given unit
  DLLEXPORT int shipAttack(_Ship* object, _Unit* Target);

//derived properties



//accessors

DLLEXPORT int getTurnNumber(Connection* c);
DLLEXPORT int getPlayerID(Connection* c);
DLLEXPORT int getGameNumber(Connection* c);
DLLEXPORT int getPirateCost(Connection* c);
DLLEXPORT int getShipCost(Connection* c);
DLLEXPORT int getPortCost(Connection* c);
DLLEXPORT int getMapSize(Connection* c);

DLLEXPORT _Pirate* getPirate(Connection* c, int num);
DLLEXPORT int getPirateCount(Connection* c);

DLLEXPORT _Player* getPlayer(Connection* c, int num);
DLLEXPORT int getPlayerCount(Connection* c);

DLLEXPORT _Port* getPort(Connection* c, int num);
DLLEXPORT int getPortCount(Connection* c);

DLLEXPORT _Ship* getShip(Connection* c, int num);
DLLEXPORT int getShipCount(Connection* c);

DLLEXPORT _Tile* getTile(Connection* c, int num);
DLLEXPORT int getTileCount(Connection* c);

DLLEXPORT _Treasure* getTreasure(Connection* c, int num);
DLLEXPORT int getTreasureCount(Connection* c);



  DLLEXPORT int networkLoop(Connection* c);
#ifdef __cplusplus
}
#endif

#endif

