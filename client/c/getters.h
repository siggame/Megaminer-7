#ifndef GETTERS_H 
#define GETTERS_H
#include "structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)
#else
#define DLLEXPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

DLLEXPORT int mappableGetId(_Mappable* ptr);
DLLEXPORT int mappableGetX(_Mappable* ptr);
DLLEXPORT int mappableGetY(_Mappable* ptr);


DLLEXPORT int unitGetId(_Unit* ptr);
DLLEXPORT int unitGetX(_Unit* ptr);
DLLEXPORT int unitGetY(_Unit* ptr);
DLLEXPORT int unitGetOwner(_Unit* ptr);
DLLEXPORT int unitGetHealth(_Unit* ptr);
DLLEXPORT int unitGetStrength(_Unit* ptr);
DLLEXPORT int unitGetMovesLeft(_Unit* ptr);
DLLEXPORT int unitGetAttacksLeft(_Unit* ptr);
DLLEXPORT int unitGetGold(_Unit* ptr);


DLLEXPORT int pirateGetId(_Pirate* ptr);
DLLEXPORT int pirateGetX(_Pirate* ptr);
DLLEXPORT int pirateGetY(_Pirate* ptr);
DLLEXPORT int pirateGetOwner(_Pirate* ptr);
DLLEXPORT int pirateGetHealth(_Pirate* ptr);
DLLEXPORT int pirateGetStrength(_Pirate* ptr);
DLLEXPORT int pirateGetMovesLeft(_Pirate* ptr);
DLLEXPORT int pirateGetAttacksLeft(_Pirate* ptr);
DLLEXPORT int pirateGetGold(_Pirate* ptr);


DLLEXPORT int playerGetId(_Player* ptr);
DLLEXPORT char* playerGetPlayerName(_Player* ptr);
DLLEXPORT int playerGetGold(_Player* ptr);
DLLEXPORT int playerGetTime(_Player* ptr);


DLLEXPORT int portGetId(_Port* ptr);
DLLEXPORT int portGetX(_Port* ptr);
DLLEXPORT int portGetY(_Port* ptr);
DLLEXPORT int portGetOwner(_Port* ptr);


DLLEXPORT int shipGetId(_Ship* ptr);
DLLEXPORT int shipGetX(_Ship* ptr);
DLLEXPORT int shipGetY(_Ship* ptr);
DLLEXPORT int shipGetOwner(_Ship* ptr);
DLLEXPORT int shipGetHealth(_Ship* ptr);
DLLEXPORT int shipGetStrength(_Ship* ptr);
DLLEXPORT int shipGetMovesLeft(_Ship* ptr);
DLLEXPORT int shipGetAttacksLeft(_Ship* ptr);
DLLEXPORT int shipGetGold(_Ship* ptr);


DLLEXPORT int tileGetId(_Tile* ptr);
DLLEXPORT int tileGetX(_Tile* ptr);
DLLEXPORT int tileGetY(_Tile* ptr);
DLLEXPORT int tileGetType(_Tile* ptr);


DLLEXPORT int treasureGetId(_Treasure* ptr);
DLLEXPORT int treasureGetX(_Treasure* ptr);
DLLEXPORT int treasureGetY(_Treasure* ptr);
DLLEXPORT int treasureGetGold(_Treasure* ptr);



#ifdef __cplusplus
}
#endif

#endif

