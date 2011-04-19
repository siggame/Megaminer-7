# -*- python -*-

from library import library

class BaseAI:
  """@brief A basic AI interface.

  This class implements most the code an AI would need to interface with the lower-level game code.
  AIs should extend this class to get a lot of builer-plate code out of the way
  The provided AI class does just that.
  """
  initialized = False
  iteration = 0
  runGenerator = None
  connection = None
  pirates = []
  players = []
  ports = []
  ships = []
  tiles = []
  treasures = []

  def startTurn(self):
    from GameObject import Pirate
    from GameObject import Player
    from GameObject import Port
    from GameObject import Ship
    from GameObject import Tile
    from GameObject import Treasure

    BaseAI.pirates = [Pirate(library.getPirate(self.connection, i)) for i in xrange(library.getPirateCount(self.connection))]
    BaseAI.players = [Player(library.getPlayer(self.connection, i)) for i in xrange(library.getPlayerCount(self.connection))]
    BaseAI.ports = [Port(library.getPort(self.connection, i)) for i in xrange(library.getPortCount(self.connection))]
    BaseAI.ships = [Ship(library.getShip(self.connection, i)) for i in xrange(library.getShipCount(self.connection))]
    BaseAI.tiles = [Tile(library.getTile(self.connection, i)) for i in xrange(library.getTileCount(self.connection))]
    BaseAI.treasures = [Treasure(library.getTreasure(self.connection, i)) for i in xrange(library.getTreasureCount(self.connection))]

    if not self.initialized:
      self.initialized = True
      self.init()
    BaseAI.iteration += 1;
    if self.runGenerator:
      try:
        return self.runGenerator.next()
      except StopIteration:
        self.runGenerator = None
    r = self.run()
    if hasattr(r, '__iter__'):
      self.runGenerator = r
      return r.next()
    return r
  
  def turnNumber(self):
    return library.getTurnNumber(self.connection)

  def playerID(self):
    return library.getPlayerID(self.connection)

  def gameNumber(self):
    return library.getGameNumber(self.connection)

  def pirateCost(self):
    return library.getPirateCost(self.connection)

  def shipCost(self):
    return library.getShipCost(self.connection)

  def portCost(self):
    return library.getPortCost(self.connection)

  def mapSize(self):
    return library.getMapSize(self.connection)

  def getPath(self, startx, starty, endx, endy, type):
    start = self.tiles[starty * self.mapSize() + startx].ptr
    end = self.tiles[endy * self.mapSize() + endx].ptr

    library.findPath(start, end, type)
    size = library.getPathSize()
    path = [self.tiles[library.getPathStep(i)] for i in xrange(size) ]

    return path

  def __init__(self, connection):
    self.connection = connection
