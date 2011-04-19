# -*-python-*-

import os

from ctypes import *

try:
  if os.name == 'posix':
    library = CDLL("./libclient.so")
  elif os.name == 'nt':
    library = CDLL("./client.dll")
  else:
    raise Exception("Unrecognized OS: "+os.name)
except OSError:
  raise Exception("It looks like you didn't build libclient. Run 'make' and try again.")

# commands

library.createConnection.restype = c_void_p
library.createConnection.argtypes = []

library.serverLogin.restype = c_int
library.serverLogin.argtypes = [c_void_p, c_char_p, c_char_p]

library.createGame.restype = c_int
library.createGame.argtypes = [c_void_p]

library.joinGame.restype = c_int
library.joinGame.argtypes = [c_void_p, c_int]

library.endTurn.restype = None
library.endTurn.argtypes = [c_void_p]

library.getStatus.restype = None
library.getStatus.argtypes = [c_void_p]

library.networkLoop.restype = c_int
library.networkLoop.argtypes = [c_void_p]

#Functions
library.unitMove.restype = c_int
library.unitMove.argtypes = [c_void_p, c_int, c_int]

library.unitTalk.restype = c_int
library.unitTalk.argtypes = [c_void_p, c_char_p]

library.unitAttack.restype = c_int
library.unitAttack.argtypes = [c_void_p, c_void_p]

library.pirateMove.restype = c_int
library.pirateMove.argtypes = [c_void_p, c_int, c_int]

library.pirateTalk.restype = c_int
library.pirateTalk.argtypes = [c_void_p, c_char_p]

library.pirateAttack.restype = c_int
library.pirateAttack.argtypes = [c_void_p, c_void_p]

library.piratePickupTreasure.restype = c_int
library.piratePickupTreasure.argtypes = [c_void_p, c_int]

library.pirateDropTreasure.restype = c_int
library.pirateDropTreasure.argtypes = [c_void_p, c_int]

library.pirateBuildPort.restype = c_int
library.pirateBuildPort.argtypes = [c_void_p]

library.portCreatePirate.restype = c_int
library.portCreatePirate.argtypes = [c_void_p]

library.portCreateShip.restype = c_int
library.portCreateShip.argtypes = [c_void_p]

library.shipMove.restype = c_int
library.shipMove.argtypes = [c_void_p, c_int, c_int]

library.shipTalk.restype = c_int
library.shipTalk.argtypes = [c_void_p, c_char_p]

library.shipAttack.restype = c_int
library.shipAttack.argtypes = [c_void_p, c_void_p]

# accessors

#Globals 
library.getTurnNumber.restype = c_int
library.getTurnNumber.argtypes = [c_void_p]

library.getPlayerID.restype = c_int
library.getPlayerID.argtypes = [c_void_p]

library.getGameNumber.restype = c_int
library.getGameNumber.argtypes = [c_void_p]

library.getPirateCost.restype = c_int
library.getPirateCost.argtypes = [c_void_p]

library.getShipCost.restype = c_int
library.getShipCost.argtypes = [c_void_p]

library.getPortCost.restype = c_int
library.getPortCost.argtypes = [c_void_p]

library.getMapSize.restype = c_int
library.getMapSize.argtypes = [c_void_p]

library.getPirate.restype = c_void_p
library.getPirate.argtypes = [c_void_p, c_int]

library.getPirateCount.restype = c_int
library.getPirateCount.argtypes = [c_void_p]

library.getPlayer.restype = c_void_p
library.getPlayer.argtypes = [c_void_p, c_int]

library.getPlayerCount.restype = c_int
library.getPlayerCount.argtypes = [c_void_p]

library.getPort.restype = c_void_p
library.getPort.argtypes = [c_void_p, c_int]

library.getPortCount.restype = c_int
library.getPortCount.argtypes = [c_void_p]

library.getShip.restype = c_void_p
library.getShip.argtypes = [c_void_p, c_int]

library.getShipCount.restype = c_int
library.getShipCount.argtypes = [c_void_p]

library.getTile.restype = c_void_p
library.getTile.argtypes = [c_void_p, c_int]

library.getTileCount.restype = c_int
library.getTileCount.argtypes = [c_void_p]

library.getTreasure.restype = c_void_p
library.getTreasure.argtypes = [c_void_p, c_int]

library.getTreasureCount.restype = c_int
library.getTreasureCount.argtypes = [c_void_p]

# getters

#Data
library.mappableGetId.restype = c_int
library.mappableGetId.argtypes = [c_void_p]

library.mappableGetX.restype = c_int
library.mappableGetX.argtypes = [c_void_p]

library.mappableGetY.restype = c_int
library.mappableGetY.argtypes = [c_void_p]

library.unitGetId.restype = c_int
library.unitGetId.argtypes = [c_void_p]

library.unitGetX.restype = c_int
library.unitGetX.argtypes = [c_void_p]

library.unitGetY.restype = c_int
library.unitGetY.argtypes = [c_void_p]

library.unitGetOwner.restype = c_int
library.unitGetOwner.argtypes = [c_void_p]

library.unitGetHealth.restype = c_int
library.unitGetHealth.argtypes = [c_void_p]

library.unitGetStrength.restype = c_int
library.unitGetStrength.argtypes = [c_void_p]

library.unitGetMovesLeft.restype = c_int
library.unitGetMovesLeft.argtypes = [c_void_p]

library.unitGetAttacksLeft.restype = c_int
library.unitGetAttacksLeft.argtypes = [c_void_p]

library.unitGetGold.restype = c_int
library.unitGetGold.argtypes = [c_void_p]

library.pirateGetId.restype = c_int
library.pirateGetId.argtypes = [c_void_p]

library.pirateGetX.restype = c_int
library.pirateGetX.argtypes = [c_void_p]

library.pirateGetY.restype = c_int
library.pirateGetY.argtypes = [c_void_p]

library.pirateGetOwner.restype = c_int
library.pirateGetOwner.argtypes = [c_void_p]

library.pirateGetHealth.restype = c_int
library.pirateGetHealth.argtypes = [c_void_p]

library.pirateGetStrength.restype = c_int
library.pirateGetStrength.argtypes = [c_void_p]

library.pirateGetMovesLeft.restype = c_int
library.pirateGetMovesLeft.argtypes = [c_void_p]

library.pirateGetAttacksLeft.restype = c_int
library.pirateGetAttacksLeft.argtypes = [c_void_p]

library.pirateGetGold.restype = c_int
library.pirateGetGold.argtypes = [c_void_p]

library.playerGetId.restype = c_int
library.playerGetId.argtypes = [c_void_p]

library.playerGetPlayerName.restype = c_char_p
library.playerGetPlayerName.argtypes = [c_void_p]

library.playerGetGold.restype = c_int
library.playerGetGold.argtypes = [c_void_p]

library.playerGetTime.restype = c_int
library.playerGetTime.argtypes = [c_void_p]

library.portGetId.restype = c_int
library.portGetId.argtypes = [c_void_p]

library.portGetX.restype = c_int
library.portGetX.argtypes = [c_void_p]

library.portGetY.restype = c_int
library.portGetY.argtypes = [c_void_p]

library.portGetOwner.restype = c_int
library.portGetOwner.argtypes = [c_void_p]

library.shipGetId.restype = c_int
library.shipGetId.argtypes = [c_void_p]

library.shipGetX.restype = c_int
library.shipGetX.argtypes = [c_void_p]

library.shipGetY.restype = c_int
library.shipGetY.argtypes = [c_void_p]

library.shipGetOwner.restype = c_int
library.shipGetOwner.argtypes = [c_void_p]

library.shipGetHealth.restype = c_int
library.shipGetHealth.argtypes = [c_void_p]

library.shipGetStrength.restype = c_int
library.shipGetStrength.argtypes = [c_void_p]

library.shipGetMovesLeft.restype = c_int
library.shipGetMovesLeft.argtypes = [c_void_p]

library.shipGetAttacksLeft.restype = c_int
library.shipGetAttacksLeft.argtypes = [c_void_p]

library.shipGetGold.restype = c_int
library.shipGetGold.argtypes = [c_void_p]

library.tileGetId.restype = c_int
library.tileGetId.argtypes = [c_void_p]

library.tileGetX.restype = c_int
library.tileGetX.argtypes = [c_void_p]

library.tileGetY.restype = c_int
library.tileGetY.argtypes = [c_void_p]

library.tileGetType.restype = c_int
library.tileGetType.argtypes = [c_void_p]

library.treasureGetId.restype = c_int
library.treasureGetId.argtypes = [c_void_p]

library.treasureGetX.restype = c_int
library.treasureGetX.argtypes = [c_void_p]

library.treasureGetY.restype = c_int
library.treasureGetY.argtypes = [c_void_p]

library.treasureGetGold.restype = c_int
library.treasureGetGold.argtypes = [c_void_p]


#utils
library.getPathSize.restype = c_int
library.getPathSize.argtypes = []

library.getPathStep.restype = c_int
library.getPathStep.argtypes = [c_int]

library.findPath.restype = c_int
library.findPath.argtypes = [c_void_p, c_void_p, c_int]
