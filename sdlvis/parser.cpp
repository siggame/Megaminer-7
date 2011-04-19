#include "parser.h"
#include "sexp/sexp.h"
#include "sexp/parser.h"
#include "sexp/sfcompat.h"

#include <cstdio>
#include <cstdlib>
#include <cstring>

#include <iostream>

using namespace std;


static bool parseMappable(Mappable& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) goto ERROR;

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.y = atoi(sub->val);
  sub = sub->next;

  return true;

  ERROR:
  cerr << "Error in parseMappable.\n Parsing: " << *expression << endl;
  return false;
}
static bool parseUnit(Unit& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) goto ERROR;

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.y = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.owner = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.health = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.strength = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.movesLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.attacksLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.gold = atoi(sub->val);
  sub = sub->next;

  return true;

  ERROR:
  cerr << "Error in parseUnit.\n Parsing: " << *expression << endl;
  return false;
}
static bool parsePirate(Pirate& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) goto ERROR;

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.y = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.owner = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.health = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.strength = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.movesLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.attacksLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.gold = atoi(sub->val);
  sub = sub->next;

  return true;

  ERROR:
  cerr << "Error in parsePirate.\n Parsing: " << *expression << endl;
  return false;
}
static bool parsePlayer(Player& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) goto ERROR;

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.playerName = new char[strlen(sub->val)+1];
  strncpy(object.playerName, sub->val, strlen(sub->val));
  object.playerName[strlen(sub->val)] = 0;
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.gold = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.time = atoi(sub->val);
  sub = sub->next;

  return true;

  ERROR:
  cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
  return false;
}
static bool parsePort(Port& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) goto ERROR;

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.y = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.owner = atoi(sub->val);
  sub = sub->next;

  return true;

  ERROR:
  cerr << "Error in parsePort.\n Parsing: " << *expression << endl;
  return false;
}
static bool parseShip(Ship& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) goto ERROR;

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.y = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.owner = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.health = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.strength = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.movesLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.attacksLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.gold = atoi(sub->val);
  sub = sub->next;

  return true;

  ERROR:
  cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
  return false;
}
static bool parseTile(Tile& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) goto ERROR;

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.y = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.type = atoi(sub->val);
  sub = sub->next;

  return true;

  ERROR:
  cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
  return false;
}
static bool parseTreasure(Treasure& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) goto ERROR;

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.y = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) goto ERROR;

  object.gold = atoi(sub->val);
  sub = sub->next;

  return true;

  ERROR:
  cerr << "Error in parseTreasure.\n Parsing: " << *expression << endl;
  return false;
}


static bool parseSexp(Game& game, sexp_t* expression)
{
  sexp_t* sub, *subsub;
  if( !expression ) return false;
  expression = expression->list;
  if( !expression ) return false;
  if(expression->val != NULL && strcmp(expression->val, "status") == 0)
  {
    GameState gs;
    while(expression->next != NULL)
    {
      expression = expression->next;
      sub = expression->list;
      if ( !sub ) return false;
      if(string(sub->val) == "game")
      {
          sub = sub->next;
          if ( !sub ) return false;
          gs.turnNumber = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.playerID = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.gameNumber = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.pirateCost = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.shipCost = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.portCost = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.mapSize = atoi(sub->val);
          sub = sub->next;
      }
      else if(string(sub->val) == "Mappable")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Mappable object;
          flag = parseMappable(object, sub);
          gs.mappables[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Unit")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Unit object;
          flag = parseUnit(object, sub);
          gs.units[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Pirate")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Pirate object;
          flag = parsePirate(object, sub);
          gs.pirates[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Player")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Player object;
          flag = parsePlayer(object, sub);
          gs.players[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Port")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Port object;
          flag = parsePort(object, sub);
          gs.ports[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Ship")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Ship object;
          flag = parseShip(object, sub);
          gs.ships[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Tile")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Tile object;
          flag = parseTile(object, sub);
          gs.tiles[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Treasure")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Treasure object;
          flag = parseTreasure(object, sub);
          gs.treasures[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
    }
    game.states.push_back(gs);
  }
  else if(string(expression->val) == "animations")
  {
    std::vector<Animation*> animations;
    while(expression->next)
    {
      expression = expression->next;
      sub = expression->list;
      if ( !sub ) return false;
    }
    game.states[game.states.size()-1].animations = animations;
  }
  else if(string(expression->val) == "ident")
  {
    expression = expression->next;
    if ( !expression ) return false;
    sub = expression->list;
    while(sub)
    {
      subsub = sub->list;
      if ( !subsub ) return false;
      int number = atoi(subsub->val);
      if(number >= 0)
      {
        subsub = subsub->next;
        if ( !subsub ) return false;
        subsub = subsub->next;
        if ( !subsub ) return false;
        game.players[number] = subsub->val;
      }
      sub = sub->next;
    }
  }
  else if(string(expression->val) == "game-winner")
  {
    expression = expression->next;
    if ( !expression ) return false;
    expression = expression->next;
    if ( !expression ) return false;
    expression = expression->next;
    if ( !expression ) return false;
    game.winner = atoi(expression->val);
		expression = expression->next;
		if( !expression ) return false;
		game.winReason = expression->val;
  }

  return true;
}


bool parseFile(Game& game, const char* filename)
{
  //bool value;
  FILE* in = fopen(filename, "r");
  //int size;
  if(!in)
    return false;

  parseFile(in);

  sexp_t* st = NULL;

  while((st = parse()))
  {
    if( !parseSexp(game, st) )
    {
      while(parse()); //empty the file, keep Lex happy.
      fclose(in);
      return false;
    }
    destroy_sexp(st);
  }

  fclose(in);

  return true;
}


bool parseString(Game& game, const char* string)
{
  sexp_t* st = NULL;

  st = extract_sexpr(string);
  bool flag = true;
  while(st && flag)
  {
    flag = parseSexp(game, st);
    destroy_sexp(st);
    st = parse();
  }

  return flag;
}
