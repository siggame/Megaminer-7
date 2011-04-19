# -*- python -*-

from library import library

from ExistentialError import ExistentialError

class GameObject(object):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self.ptr = ptr
    self.iteration = BaseAI.iteration


##An object that exists on the grid
class Mappable(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self.ptr = ptr
    self.iteration = BaseAI.iteration
    
    self.id = library.mappableGetId(ptr)

  ##Unique Identifier
  def getId(self):
    self.validify()
    return library.mappableGetId(self.ptr)

  ##The X position of this object.  X is horizontal, with 0,0 as the top left corner
  def getX(self):
    self.validify()
    return library.mappableGetX(self.ptr)

  ##The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  def getY(self):
    self.validify()
    return library.mappableGetY(self.ptr)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    return ret

##Generic Unit
class Unit(Mappable):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self.ptr = ptr
    self.iteration = BaseAI.iteration
    
    self.id = library.unitGetId(ptr)

  ##Move the unit to the designated X and Y coordinates if possible
  def move(self, x, y):
    self.validify()
    return library.unitMove(self.ptr, x, y)

  ##Allows a unit to display a message to the screen.
  def talk(self, message):
    self.validify()
    return library.unitTalk(self.ptr, message)

  ##Attempt to attack the input target if possible
  def attack(self, Target):
    self.validify()
    if not isinstance(Target, Unit):
      raise TypeError('Target should be of [Unit]')
    Target.validify()
    return library.unitAttack(self.ptr, Target.ptr)

  ##Unique Identifier
  def getId(self):
    self.validify()
    return library.unitGetId(self.ptr)

  ##The X position of this object.  X is horizontal, with 0,0 as the top left corner
  def getX(self):
    self.validify()
    return library.unitGetX(self.ptr)

  ##The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  def getY(self):
    self.validify()
    return library.unitGetY(self.ptr)

  ##Represents the owner of the unit.
  def getOwner(self):
    self.validify()
    return library.unitGetOwner(self.ptr)

  ##Current ealth of the unit
  def getHealth(self):
    self.validify()
    return library.unitGetHealth(self.ptr)

  ##Attacking strength of the unit (Each point of strength deals 1 health of damage)
  def getStrength(self):
    self.validify()
    return library.unitGetStrength(self.ptr)

  ##Displays the remaining moves for this unit this turn
  def getMovesLeft(self):
    self.validify()
    return library.unitGetMovesLeft(self.ptr)

  ##Displays the remaining attacks for this unit this turn
  def getAttacksLeft(self):
    self.validify()
    return library.unitGetAttacksLeft(self.ptr)

  ##Amount of gold carried by the unit.
  def getGold(self):
    self.validify()
    return library.unitGetGold(self.ptr)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "owner: %s\n" % self.getOwner()
    ret += "health: %s\n" % self.getHealth()
    ret += "strength: %s\n" % self.getStrength()
    ret += "movesLeft: %s\n" % self.getMovesLeft()
    ret += "attacksLeft: %s\n" % self.getAttacksLeft()
    ret += "gold: %s\n" % self.getGold()
    return ret

##A basic pirate. These units are bound to land unless aboard a ship. they can pickup and drop treasure as well as build ports and fight other pirates.
class Pirate(Unit):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self.ptr = ptr
    self.iteration = BaseAI.iteration
    
    self.id = library.pirateGetId(ptr)

  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self.iteration == BaseAI.iteration:
      return True
    for i in BaseAI.pirates:
      if i.id == self.id:
        self.ptr = i.ptr
        self.iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  ##Move the unit to the designated X and Y coordinates if possible
  def move(self, x, y):
    self.validify()
    return library.pirateMove(self.ptr, x, y)

  ##Allows a unit to display a message to the screen.
  def talk(self, message):
    self.validify()
    return library.pirateTalk(self.ptr, message)

  ##Attempt to attack the input target if possible
  def attack(self, Target):
    self.validify()
    if not isinstance(Target, Unit):
      raise TypeError('Target should be of [Unit]')
    Target.validify()
    return library.pirateAttack(self.ptr, Target.ptr)

  ##Allows the pirate to pickup treasure on the ground.
  def pickupTreasure(self, amount):
    self.validify()
    return library.piratePickupTreasure(self.ptr, amount)

  ##Allows the pirate to drop treasure they are carrying.
  def dropTreasure(self, amount):
    self.validify()
    return library.pirateDropTreasure(self.ptr, amount)

  ##Pirate builds a port on a land tile with water tile adjacent. Cannot be within three spaces of another port!
  def buildPort(self):
    self.validify()
    return library.pirateBuildPort(self.ptr)

  ##Unique Identifier
  def getId(self):
    self.validify()
    return library.pirateGetId(self.ptr)

  ##The X position of this object.  X is horizontal, with 0,0 as the top left corner
  def getX(self):
    self.validify()
    return library.pirateGetX(self.ptr)

  ##The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  def getY(self):
    self.validify()
    return library.pirateGetY(self.ptr)

  ##Represents the owner of the unit.
  def getOwner(self):
    self.validify()
    return library.pirateGetOwner(self.ptr)

  ##Current ealth of the unit
  def getHealth(self):
    self.validify()
    return library.pirateGetHealth(self.ptr)

  ##Attacking strength of the unit (Each point of strength deals 1 health of damage)
  def getStrength(self):
    self.validify()
    return library.pirateGetStrength(self.ptr)

  ##Displays the remaining moves for this unit this turn
  def getMovesLeft(self):
    self.validify()
    return library.pirateGetMovesLeft(self.ptr)

  ##Displays the remaining attacks for this unit this turn
  def getAttacksLeft(self):
    self.validify()
    return library.pirateGetAttacksLeft(self.ptr)

  ##Amount of gold carried by the unit.
  def getGold(self):
    self.validify()
    return library.pirateGetGold(self.ptr)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "owner: %s\n" % self.getOwner()
    ret += "health: %s\n" % self.getHealth()
    ret += "strength: %s\n" % self.getStrength()
    ret += "movesLeft: %s\n" % self.getMovesLeft()
    ret += "attacksLeft: %s\n" % self.getAttacksLeft()
    ret += "gold: %s\n" % self.getGold()
    return ret

##
class Player(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self.ptr = ptr
    self.iteration = BaseAI.iteration
    
    self.id = library.playerGetId(ptr)

  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self.iteration == BaseAI.iteration:
      return True
    for i in BaseAI.players:
      if i.id == self.id:
        self.ptr = i.ptr
        self.iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  ##Unique Identifier
  def getId(self):
    self.validify()
    return library.playerGetId(self.ptr)

  ##Player's Name
  def getPlayerName(self):
    self.validify()
    return library.playerGetPlayerName(self.ptr)

  ##Player's Gold
  def getGold(self):
    self.validify()
    return library.playerGetGold(self.ptr)

  ##Time remaining
  def getTime(self):
    self.validify()
    return library.playerGetTime(self.ptr)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "playerName: %s\n" % self.getPlayerName()
    ret += "gold: %s\n" % self.getGold()
    ret += "time: %s\n" % self.getTime()
    return ret

##A basic port. The port can create new pirates and ships and is used when pirates need to deposit money.
class Port(Mappable):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self.ptr = ptr
    self.iteration = BaseAI.iteration
    
    self.id = library.portGetId(ptr)

  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self.iteration == BaseAI.iteration:
      return True
    for i in BaseAI.ports:
      if i.id == self.id:
        self.ptr = i.ptr
        self.iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  ##Creates a Pirate at the calling Port
  def createPirate(self):
    self.validify()
    return library.portCreatePirate(self.ptr)

  ##Creates a Ship at the calling Port
  def createShip(self):
    self.validify()
    return library.portCreateShip(self.ptr)

  ##Unique Identifier
  def getId(self):
    self.validify()
    return library.portGetId(self.ptr)

  ##The X position of this object.  X is horizontal, with 0,0 as the top left corner
  def getX(self):
    self.validify()
    return library.portGetX(self.ptr)

  ##The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  def getY(self):
    self.validify()
    return library.portGetY(self.ptr)

  ##The ownder of the port
  def getOwner(self):
    self.validify()
    return library.portGetOwner(self.ptr)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "owner: %s\n" % self.getOwner()
    return ret

##A basic ship. They can only travel by sea and attack other ships. Whenever the ship moves, any pirates on his tile go with it
class Ship(Unit):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self.ptr = ptr
    self.iteration = BaseAI.iteration
    
    self.id = library.shipGetId(ptr)

  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self.iteration == BaseAI.iteration:
      return True
    for i in BaseAI.ships:
      if i.id == self.id:
        self.ptr = i.ptr
        self.iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  ##Move the unit to the designated X and Y coordinates if possible
  def move(self, x, y):
    self.validify()
    return library.shipMove(self.ptr, x, y)

  ##Allows a unit to display a message to the screen.
  def talk(self, message):
    self.validify()
    return library.shipTalk(self.ptr, message)

  ##Attempt to attack the input target if possible
  def attack(self, Target):
    self.validify()
    if not isinstance(Target, Unit):
      raise TypeError('Target should be of [Unit]')
    Target.validify()
    return library.shipAttack(self.ptr, Target.ptr)

  ##Unique Identifier
  def getId(self):
    self.validify()
    return library.shipGetId(self.ptr)

  ##The X position of this object.  X is horizontal, with 0,0 as the top left corner
  def getX(self):
    self.validify()
    return library.shipGetX(self.ptr)

  ##The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  def getY(self):
    self.validify()
    return library.shipGetY(self.ptr)

  ##Represents the owner of the unit.
  def getOwner(self):
    self.validify()
    return library.shipGetOwner(self.ptr)

  ##Current ealth of the unit
  def getHealth(self):
    self.validify()
    return library.shipGetHealth(self.ptr)

  ##Attacking strength of the unit (Each point of strength deals 1 health of damage)
  def getStrength(self):
    self.validify()
    return library.shipGetStrength(self.ptr)

  ##Displays the remaining moves for this unit this turn
  def getMovesLeft(self):
    self.validify()
    return library.shipGetMovesLeft(self.ptr)

  ##Displays the remaining attacks for this unit this turn
  def getAttacksLeft(self):
    self.validify()
    return library.shipGetAttacksLeft(self.ptr)

  ##Amount of gold carried by the unit.
  def getGold(self):
    self.validify()
    return library.shipGetGold(self.ptr)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "owner: %s\n" % self.getOwner()
    ret += "health: %s\n" % self.getHealth()
    ret += "strength: %s\n" % self.getStrength()
    ret += "movesLeft: %s\n" % self.getMovesLeft()
    ret += "attacksLeft: %s\n" % self.getAttacksLeft()
    ret += "gold: %s\n" % self.getGold()
    return ret

##A basic tile
class Tile(Mappable):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self.ptr = ptr
    self.iteration = BaseAI.iteration
    
    self.id = library.tileGetId(ptr)

  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self.iteration == BaseAI.iteration:
      return True
    for i in BaseAI.tiles:
      if i.id == self.id:
        self.ptr = i.ptr
        self.iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  ##Unique Identifier
  def getId(self):
    self.validify()
    return library.tileGetId(self.ptr)

  ##The X position of this object.  X is horizontal, with 0,0 as the top left corner
  def getX(self):
    self.validify()
    return library.tileGetX(self.ptr)

  ##The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  def getY(self):
    self.validify()
    return library.tileGetY(self.ptr)

  ##land = 0, water = 1
  def getType(self):
    self.validify()
    return library.tileGetType(self.ptr)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "type: %s\n" % self.getType()
    return ret

##This is the source of your wealth. When dropped on the ground it will build interest baed on its distance to pirates, if dropped on a port it is added to your ooverall wealth
class Treasure(Mappable):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self.ptr = ptr
    self.iteration = BaseAI.iteration
    
    self.id = library.treasureGetId(ptr)

  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self.iteration == BaseAI.iteration:
      return True
    for i in BaseAI.treasures:
      if i.id == self.id:
        self.ptr = i.ptr
        self.iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  ##Unique Identifier
  def getId(self):
    self.validify()
    return library.treasureGetId(self.ptr)

  ##The X position of this object.  X is horizontal, with 0,0 as the top left corner
  def getX(self):
    self.validify()
    return library.treasureGetX(self.ptr)

  ##The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  def getY(self):
    self.validify()
    return library.treasureGetY(self.ptr)

  ##The amount of gold currently with this treasure
  def getGold(self):
    self.validify()
    return library.treasureGetGold(self.ptr)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "gold: %s\n" % self.getGold()
    return ret
