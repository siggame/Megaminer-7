from objectHolder import ObjectHolder

class GameWorld(object):
  """
  Base class for a game world object
  """
  def __init__(self):
    self.nextid = 0
    self.maxid = 2147483647
    self.turnNumber = 0
    self.players = []
    self.spectators = []
    self.turn = None #the player whose turn it is;
             #None before and after the game.
    self.winner = None #the player who won the game;
               #None before and during the game
    self.objects = ObjectHolder() #key: object's id
                #value: instance of the object
    self.animations = ["animations"]

  def addObject(self, newObject):
    self.animations += [["add", newObject.id]]
    self.objects[newObject.id] = newObject

  def removeObject(self, oldObject):
    self.animations += [["remove", oldObject.id]]
    del self.objects[oldObject.id]

DefaultGameWorld = GameWorld
