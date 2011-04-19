//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#pragma warning(disable : 4996)

#include <string>
#include <cstring>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <fstream>
#include <memory>

#include "game.h"
#include "network.h"
#include "structures.h"

#include "sexp/sfcompat.h"

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

#ifdef _WIN32
//Doh, namespace collision.
namespace Windows
{
    #include <Windows.h>
};
#else
#include <unistd.h>
#endif

#ifdef ENABLE_THREADS 
#define LOCK(X) pthread_mutex_lock(X)
#define UNLOCK(X) pthread_mutex_unlock(X)
#else
#define LOCK(X)
#define UNLOCK(X)
#endif

using namespace std;

DLLEXPORT Connection* createConnection()
{
  Connection* c = new Connection;
  c->socket = -1;
  #ifdef ENABLE_THREADS 
  pthread_mutex_init(&c->mutex, NULL);
  #endif
  
  c->turnNumber = 0;
  c->playerID = 0;
  c->gameNumber = 0;
  c->pirateCost = 0;
  c->shipCost = 0;
  c->portCost = 0;
  c->mapSize = 0;
  c->Pirates = NULL;
  c->PirateCount = 0;
  c->Players = NULL;
  c->PlayerCount = 0;
  c->Ports = NULL;
  c->PortCount = 0;
  c->Ships = NULL;
  c->ShipCount = 0;
  c->Tiles = NULL;
  c->TileCount = 0;
  c->Treasures = NULL;
  c->TreasureCount = 0;
  return c;
}

DLLEXPORT void destroyConnection(Connection* c)
{
  #ifdef ENABLE_THREADS 
  pthread_mutex_destroy(&c->mutex);
  #endif 
  if(c->Pirates)
  {
    for(int i = 0; i < c->PirateCount; i++)
    {
    }
    delete[] c->Pirates;
  }
  if(c->Players)
  {
    for(int i = 0; i < c->PlayerCount; i++)
    {
      delete[] c->Players[i].playerName;
    }
    delete[] c->Players;
  }
  if(c->Ports)
  {
    for(int i = 0; i < c->PortCount; i++)
    {
    }
    delete[] c->Ports;
  }
  if(c->Ships)
  {
    for(int i = 0; i < c->ShipCount; i++)
    {
    }
    delete[] c->Ships;
  }
  if(c->Tiles)
  {
    for(int i = 0; i < c->TileCount; i++)
    {
    }
    delete[] c->Tiles;
  }
  if(c->Treasures)
  {
    for(int i = 0; i < c->TreasureCount; i++)
    {
    }
    delete[] c->Treasures;
  }
  delete c;
}

DLLEXPORT int serverConnect(Connection* c, const char* host, const char* port)
{
  c->socket = open_server_connection(host, port);
  return c->socket + 1; //false if socket == -1
}

DLLEXPORT int serverLogin(Connection* c, const char* username, const char* password)
{
  string expr = "(login \"";
  expr += username;
  expr += "\" \"";
  expr += password;
  expr +="\")";

  send_string(c->socket, expr.c_str());

  sexp_t* expression, *message;

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;
  
  message = expression->list;
  if(message->val == NULL || strcmp(message->val, "login-accepted") != 0)
  {
    cerr << "Unable to login to server" << endl;
    destroy_sexp(expression);
    return 0;
  }
  destroy_sexp(expression);
  return 1;
}

DLLEXPORT int createGame(Connection* c)
{
  sexp_t* expression, *number;

  send_string(c->socket, "(create-game)");
  
  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;
  
  number = expression->list->next;
  c->gameNumber = atoi(number->val);
  destroy_sexp(expression);
  
  std::cout << "Creating game " << c->gameNumber << endl;
  
  c->playerID = 0;
  
  return c->gameNumber;
}

DLLEXPORT int joinGame(Connection* c, int gameNum)
{
  sexp_t* expression;
  stringstream expr;
  
  c->gameNumber = gameNum;
  
  expr << "(join-game " << c->gameNumber << ")";
  send_string(c->socket, expr.str().c_str());
  
  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;
  
  if(strcmp(expression->list->val, "join-accepted") != 0)
  {
    cerr << "Game " << c->gameNumber << " doesn't exist." << endl;
    destroy_sexp(expression);
    return 0;
  }
  destroy_sexp(expression);
  
  c->playerID = 1;
  send_string(c->socket, "(game-start)");
  
  return 1;
}

DLLEXPORT void endTurn(Connection* c)
{
  LOCK( &c->mutex );
  send_string(c->socket, "(end-turn)");
  UNLOCK( &c->mutex );
}

DLLEXPORT void getStatus(Connection* c)
{
  LOCK( &c->mutex );
  send_string(c->socket, "(game-status)");
  UNLOCK( &c->mutex );
}

static void pirateShip( Connection * c,int x, int y, int futureOwner)
{
  int count = 0;
  // look for a pirate at either the start or end location
  for(int i=0; i < c->PirateCount && count<2; i++)
  {
    if(c->Pirates[i].health > 0 && c->Pirates[i].x == x && c->Pirates[i].y == y)
    {
      count++;
    }
  }
  // Look for ships if either are true
  for(int i=0; i < c->ShipCount && count < 2; i++)
  {
    // there is a ship at your starting location, and you were the only pirate on it
    if(c->Ships[i].x == x && c->Ships[i].y == y)
    {
      c->Ships[i].owner = futureOwner;
      // stop looking for a ship
      count=2;
    }
  }
}

DLLEXPORT int unitMove(_Unit* object, int x, int y)
{
  stringstream expr;
  expr << "(game-move " << object->id
       << " " << x
       << " " << y
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  return 1;
}

DLLEXPORT int unitTalk(_Unit* object, char* message)
{
  stringstream expr;
  expr << "(game-talk " << object->id
      << " \"" << escape_string(message) << "\""
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  return 1;
}

DLLEXPORT int unitAttack(_Unit* object, _Unit* Target)
{
  stringstream expr;
  expr << "(game-attack " << object->id
      << " " << Target->id
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  return 1;
}


DLLEXPORT int pirateMove(_Pirate* object, int x, int y)
{
  stringstream expr;
  expr << "(game-move " << object->id
       << " " << x
       << " " << y
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  
  // Game state changes

  // leaving the ship
  pirateShip(object->_c, object->x,object->y,-1);
  // entering a ship
  pirateShip(object->_c, x,y,object->owner);
  object->x = x;
  object->y = y;
  object->movesLeft--;
  
  return 1;
}

DLLEXPORT int pirateTalk(_Pirate* object, char* message)
{
  stringstream expr;
  expr << "(game-talk " << object->id
      << " \"" << escape_string(message) << "\""
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  
  return 1;
}

DLLEXPORT int pirateAttack(_Pirate* object, _Unit* Target)
{
  stringstream expr;
  expr << "(game-attack " << object->id
      << " " << Target->id
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  // Game state changes
  if(Target->health > 0 && (Target->health-=object->strength)<=0)
  {
    // get their gold
    object->gold+=Target->gold;
    Target->gold=0;
    // handle ship ownership
    pirateShip(object->_c, Target->x, Target->y,-1);
  }
  object->attacksLeft--;
  
  return 1;
}

DLLEXPORT int piratePickupTreasure(_Pirate* object, int amount)
{
  stringstream expr;
  expr << "(game-pickup-treasure " << object->id
       << " " << amount
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  // Game state changes
  Connection * c = object->_c;

  object->gold+=amount;
  bool found = false;
  // Look through the treasures for one that is at this location
  for(int i=0;!found && i<c->ShipCount;i++)
  {
    // if that Ship is at this spot
    if(c->Ships[i].x == object->x && c->Ships[i].y == object->y)
    {
      c->Ships[i].gold-=amount;
      found = true;
    }
  }
  // Look through the ports
  for(int i=0;!found && i<c->PortCount;i++)
  {
    // if that Port is at this spot
    if(c->Ports[i].x == object->x && c->Ports[i].y == object->y)
    {
      c->Players[c->playerID].gold-=amount;
      found = true;
    }
  }
  // Look through the Treasures
  for(int i=0;!found && i<c->TreasureCount;i++)
  {
    // if that treasure is at this spot
    if(c->Treasures[i].x == object->x && c->Treasures[i].y == object->y)
    {
      c->Treasures[i].gold-=amount;
      found = true;
    }
  }
  return 1;
}

DLLEXPORT int pirateDropTreasure(_Pirate* object, int amount)
{
  stringstream expr;
  expr << "(game-drop-treasure " << object->id
       << " " << amount
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  // Game state changes
  Connection * c = object->_c;

  object->gold-=amount;
  bool found = false;
  // Look through the treasures for one that is at this location
  for(int i=0;!found && i<c->ShipCount;i++)
  {
    // if that Ship is at this spot
    if(c->Ships[i].x == object->x && c->Ships[i].y == object->y)
    {
      c->Ships[i].gold+=amount;
      found = true;
    }
  }
  // Look through the ports
  for(int i=0;!found && i<c->PortCount;i++)
  {
    // if that Port is at this spot
    if(c->Ports[i].x == object->x && c->Ports[i].y == object->y)
    {
      c->Players[c->playerID].gold+=amount;
      found = true;
    }
  }
  // Look through the Treasures
  for(int i=0;!found && i<c->TreasureCount;i++)
  {
    // if that treasure is at this spot
    if(c->Treasures[i].x == object->x && c->Treasures[i].y == object->y)
    {
      c->Treasures[i].gold+=amount;
      found = true;
    }
  }
  return 1;
}

DLLEXPORT int pirateBuildPort(_Pirate* object)
{
  stringstream expr;
  expr << "(game-build-port " << object->id
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  // Game state changes
  Connection* c = object->_c;
  c->Players[c->playerID].gold-=c->portCost;
  return 1;
}



DLLEXPORT int portCreatePirate(_Port* object)
{
  stringstream expr;
  expr << "(game-create-pirate " << object->id
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  // Game state changes
  Connection* c = object->_c;
  c->Players[c->playerID].gold-=c->pirateCost;
  pirateShip(object->_c, object->x, object->y, object->owner);
  return 1;
}

DLLEXPORT int portCreateShip(_Port* object)
{
  stringstream expr;
  expr << "(game-create-ship " << object->id
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  // Game state changes
  Connection* c = object->_c;
  c->Players[c->playerID].gold-=c->shipCost;
  return 1;
}


DLLEXPORT int shipMove(_Ship* object, int x, int y)
{
  stringstream expr;
  expr << "(game-move " << object->id
       << " " << x
       << " " << y
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  // Game state changes
  Connection * c = object->_c;
  
  for(int i=0;i<c->PirateCount;i++)
  {
    // move the pirate standing on this dude
    if(c->Pirates[i].x == object->x && c->Pirates[i].y == object->y)
    {
      c->Pirates[i].x = x;
      c->Pirates[i].y = y;
    }
  }
  object->x = x;
  object->y = y;
  object->movesLeft--;
  return 1;
}

DLLEXPORT int shipTalk(_Ship* object, char* message)
{
  stringstream expr;
  expr << "(game-talk " << object->id
      << " \"" << escape_string(message) << "\""
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  // Game state changes
  return 1;
}

DLLEXPORT int shipAttack(_Ship* object, _Unit* Target)
{
  stringstream expr;
  expr << "(game-attack " << object->id
      << " " << Target->id
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  // Game state changes
  Target->health-=object->strength;
  object->attacksLeft--;
  return 1;
}




//Utility functions for parsing data
void parseMappable(Connection* c, _Mappable* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;
  
  object->_c = c;
  
  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  
}
void parseUnit(Connection* c, _Unit* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;
  
  object->_c = c;
  
  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  object->owner = atoi(sub->val);
  sub = sub->next;
  object->health = atoi(sub->val);
  sub = sub->next;
  object->strength = atoi(sub->val);
  sub = sub->next;
  object->movesLeft = atoi(sub->val);
  sub = sub->next;
  object->attacksLeft = atoi(sub->val);
  sub = sub->next;
  object->gold = atoi(sub->val);
  sub = sub->next;
  
}
void parsePirate(Connection* c, _Pirate* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;
  
  object->_c = c;
  
  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  object->owner = atoi(sub->val);
  sub = sub->next;
  object->health = atoi(sub->val);
  sub = sub->next;
  object->strength = atoi(sub->val);
  sub = sub->next;
  object->movesLeft = atoi(sub->val);
  sub = sub->next;
  object->attacksLeft = atoi(sub->val);
  sub = sub->next;
  object->gold = atoi(sub->val);
  sub = sub->next;
  
}
void parsePlayer(Connection* c, _Player* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;
  
  object->_c = c;
  
  object->id = atoi(sub->val);
  sub = sub->next;
  object->playerName = new char[strlen(sub->val)+1];
  strncpy(object->playerName, sub->val, strlen(sub->val));
  object->playerName[strlen(sub->val)] = 0;
  sub = sub->next;
  object->gold = atoi(sub->val);
  sub = sub->next;
  object->time = atoi(sub->val);
  sub = sub->next;
  
}
void parsePort(Connection* c, _Port* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;
  
  object->_c = c;
  
  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  object->owner = atoi(sub->val);
  sub = sub->next;
  
}
void parseShip(Connection* c, _Ship* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;
  
  object->_c = c;
  
  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  object->owner = atoi(sub->val);
  sub = sub->next;
  object->health = atoi(sub->val);
  sub = sub->next;
  object->strength = atoi(sub->val);
  sub = sub->next;
  object->movesLeft = atoi(sub->val);
  sub = sub->next;
  object->attacksLeft = atoi(sub->val);
  sub = sub->next;
  object->gold = atoi(sub->val);
  sub = sub->next;
  
}
void parseTile(Connection* c, _Tile* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;
  
  object->_c = c;
  
  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  object->type = atoi(sub->val);
  sub = sub->next;
  
}
void parseTreasure(Connection* c, _Treasure* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;
  
  object->_c = c;
  
  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  object->gold = atoi(sub->val);
  sub = sub->next;
  
}

DLLEXPORT int networkLoop(Connection* c)
{
  while(true)
  {
    sexp_t* base, *expression, *sub, *subsub;
    
    char* message = rec_string(c->socket);
    string text = message;
    base = extract_sexpr(message);
    delete[] message;
    expression = base->list;
    if(expression->val != NULL && strcmp(expression->val, "game-winner") == 0)
    {
      expression = expression->next->next->next;
      int winnerID = atoi(expression->val);
      if(winnerID == c->playerID)
      {
        cout << "You win!" << endl << expression->next->val << endl;
      }
      else
      {
        cout << "You lose. :(" << endl << expression->next->val << endl;
      }
      stringstream expr;
      expr << "(request-log " << c->gameNumber << ")";
      send_string(c->socket, expr.str().c_str());
      destroy_sexp(base);
      return 0;
    }
    else if(expression->val != NULL && strcmp(expression->val, "log") == 0)
    {
      ofstream out;
      stringstream filename;
      expression = expression->next;
      filename << expression->val;
      filename << ".gamelog";
      expression = expression->next;
      out.open(filename.str().c_str());
      if (out.good())
        out.write(expression->val, strlen(expression->val));
      else
        cerr << "Error : Could not create log." << endl;
      out.close();
      destroy_sexp(base);
      return 0;
    }
    else if(expression->val != NULL && strcmp(expression->val, "game-accepted")==0)
    {
      char gameID[30];

      expression = expression->next;
      strcpy(gameID, expression->val);
      cout << "Created game " << gameID << endl;
    }
    else if(expression->val != NULL && strstr(expression->val, "denied"))
    {
      cout << expression->val << endl;
      cout << expression->next->val << endl;
    }
    else if(expression->val != NULL && strcmp(expression->val, "status") == 0)
    {
      while(expression->next != NULL)
      {
        expression = expression->next;
        sub = expression->list;
        if(string(sub->val) == "game")
        {
          sub = sub->next;
          c->turnNumber = atoi(sub->val);
          sub = sub->next;

          c->playerID = atoi(sub->val);
          sub = sub->next;

          c->gameNumber = atoi(sub->val);
          sub = sub->next;

          c->pirateCost = atoi(sub->val);
          sub = sub->next;

          c->shipCost = atoi(sub->val);
          sub = sub->next;

          c->portCost = atoi(sub->val);
          sub = sub->next;

          c->mapSize = atoi(sub->val);
          sub = sub->next;

        }
        else if(string(sub->val) == "Pirate")
        {
          if(c->Pirates)
          {
            for(int i = 0; i < c->PirateCount; i++)
            {
            }
            delete[] c->Pirates;
          }
          c->PirateCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Pirates = new _Pirate[c->PirateCount];
          for(int i = 0; i < c->PirateCount; i++)
          {
            sub = sub->next;
            parsePirate(c, c->Pirates+i, sub);
          }
        }
        else if(string(sub->val) == "Player")
        {
          if(c->Players)
          {
            for(int i = 0; i < c->PlayerCount; i++)
            {
              delete[] c->Players[i].playerName;
            }
            delete[] c->Players;
          }
          c->PlayerCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Players = new _Player[c->PlayerCount];
          for(int i = 0; i < c->PlayerCount; i++)
          {
            sub = sub->next;
            parsePlayer(c, c->Players+i, sub);
          }
        }
        else if(string(sub->val) == "Port")
        {
          if(c->Ports)
          {
            for(int i = 0; i < c->PortCount; i++)
            {
            }
            delete[] c->Ports;
          }
          c->PortCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Ports = new _Port[c->PortCount];
          for(int i = 0; i < c->PortCount; i++)
          {
            sub = sub->next;
            parsePort(c, c->Ports+i, sub);
          }
        }
        else if(string(sub->val) == "Ship")
        {
          if(c->Ships)
          {
            for(int i = 0; i < c->ShipCount; i++)
            {
            }
            delete[] c->Ships;
          }
          c->ShipCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Ships = new _Ship[c->ShipCount];
          for(int i = 0; i < c->ShipCount; i++)
          {
            sub = sub->next;
            parseShip(c, c->Ships+i, sub);
          }
        }
        else if(string(sub->val) == "Tile")
        {
          if(c->Tiles)
          {
            for(int i = 0; i < c->TileCount; i++)
            {
            }
            delete[] c->Tiles;
          }
          c->TileCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Tiles = new _Tile[c->TileCount];
          for(int i = 0; i < c->TileCount; i++)
          {
            sub = sub->next;
            parseTile(c, c->Tiles+i, sub);
          }
        }
        else if(string(sub->val) == "Treasure")
        {
          if(c->Treasures)
          {
            for(int i = 0; i < c->TreasureCount; i++)
            {
            }
            delete[] c->Treasures;
          }
          c->TreasureCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Treasures = new _Treasure[c->TreasureCount];
          for(int i = 0; i < c->TreasureCount; i++)
          {
            sub = sub->next;
            parseTreasure(c, c->Treasures+i, sub);
          }
        }
      }
      destroy_sexp(base);
      return 1;
    }
    else
    {
#ifdef SHOW_WARNINGS
      cerr << "Unrecognized message: " << text << endl;
#endif
    }
    destroy_sexp(base);
  }
}

DLLEXPORT _Pirate* getPirate(Connection* c, int num)
{
  return c->Pirates + num;
}
DLLEXPORT int getPirateCount(Connection* c)
{
  return c->PirateCount;
}

DLLEXPORT _Player* getPlayer(Connection* c, int num)
{
  return c->Players + num;
}
DLLEXPORT int getPlayerCount(Connection* c)
{
  return c->PlayerCount;
}

DLLEXPORT _Port* getPort(Connection* c, int num)
{
  return c->Ports + num;
}
DLLEXPORT int getPortCount(Connection* c)
{
  return c->PortCount;
}

DLLEXPORT _Ship* getShip(Connection* c, int num)
{
  return c->Ships + num;
}
DLLEXPORT int getShipCount(Connection* c)
{
  return c->ShipCount;
}

DLLEXPORT _Tile* getTile(Connection* c, int num)
{
  return c->Tiles + num;
}
DLLEXPORT int getTileCount(Connection* c)
{
  return c->TileCount;
}

DLLEXPORT _Treasure* getTreasure(Connection* c, int num)
{
  return c->Treasures + num;
}
DLLEXPORT int getTreasureCount(Connection* c)
{
  return c->TreasureCount;
}


DLLEXPORT int getTurnNumber(Connection* c)
{
  return c->turnNumber;
}
DLLEXPORT int getPlayerID(Connection* c)
{
  return c->playerID;
}
DLLEXPORT int getGameNumber(Connection* c)
{
  return c->gameNumber;
}
DLLEXPORT int getPirateCost(Connection* c)
{
  return c->pirateCost;
}
DLLEXPORT int getShipCost(Connection* c)
{
  return c->shipCost;
}
DLLEXPORT int getPortCost(Connection* c)
{
  return c->portCost;
}
DLLEXPORT int getMapSize(Connection* c)
{
  return c->mapSize;
}

