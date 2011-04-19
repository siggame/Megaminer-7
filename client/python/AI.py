#-*-python-*-
from BaseAI import BaseAI

import random

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  
  #Set this return value to be your team username as configured on megaminerai.com
  def username():
    return "Shell AI"

  #Set this return value to be your team password as configured on megaminerai.com
  @staticmethod
  def password():
    return "password"

  #things that happen before your turn begins
  def init(self):
    print "Initializing"

  #Things that happen after your turn has ended
  def end(self):
    pass

  #Things that happen during your turn.
  def run(self):
  
    #----------------------------------------------------------------------
    #Pre-Defined Data Structures : 
    #List of type Pirate named pirates
    #List of type Ship named ships
    #List of type Port named ports
    #List of type Tile named tiles
    #List of type Treasure named treasures
    
    #If you need clarification on python, please find a dev
    #----------------------------------------------------------------------
    
    #----------------------------------------------------------------------
    #Port Functions:   
    #WHERE CALLING OBJECT IS A PORT
    
    #getId()
      #Unique Identifier
    
    #getX()
      #The X position of this object.  X is horizontal, with 0,0 as the top left corner
        
    #getY()
      #The Y position of this object.  Y is vertical, with 0,0 as the top left corner
        
    #getOwner()
      #The owner of the port
      
    #createPirate()
      #creates a pirate at the calling port
      
    #createShip()
      #creates a ship at the calling port
    #----------------------------------------------------------------------
    
    #----------------------------------------------------------------------  
    #Pirate/Ship Functions:
    #WHERE CALLING OBJECT IS A PIRATE OR SHIP
    
    #getId()
      #Unique Identifier
    
    #getX()
      #The X position of this object.  X is horizontal, with 0,0 as the top left corner
    
    #getY()
      #The Y position of this object.  Y is vertical, with 0,0 as the top left corner
    
    #getOwner()
      #The owner of the unit
    
    #getHealth()
      #health of the unit
    
    #getStrength()
      #attacking strength of the unit
    
    #getMovesLeft()
      #Attacks left this turn for the unit
    
    #getAttacksLeft()
      #Moves left this turn for the unit
      
    #getGold()
      #Amoutn of gold the unit is carrying
      
    #attack(target)
      #Attacks the passed in unit if possible
      
    #move(x,y)
      #Moves to the passed in location if possible
      
    #createPort() (ONLY FOR PIRATES)
      #Creates a port at the pirate's current location if possible 
      
    #pickupTreasure(goldAmount) (ONLY FOR PIRATES)
      #Picks up gold from the ground or from a port
    
    #dropTreasure(goldAmount) (ONLY FOR PIRATES)
      #Pirate drops its gold
    #----------------------------------------------------------------------
    
    #----------------------------------------------------------------------
    #Tile Functions:
    #WHERE CALLING OBJECT IS OF TYPE TILE
    
    #getId()
      #Unique Identifier
      
    #getX()
      #The X position of this object.  X is horizontal, with 0,0 as the top left corner
      
    #getY()
      #The Y position of this object.  Y is vertical, with 0,0 as the top left corner
      
    #getType()
      #land = 0, water = 1
    #----------------------------------------------------------------------
    
    #----------------------------------------------------------------------  
    #Treasure Functions:
    #WHERE CALLING OBJECT IS OF TYPE TREASURE
    
    #getId()
      #Unique Identifier

    #getX()
      #The X position of this object.  X is horizontal, with 0,0 as the top left corner
      
    #getY()
      #The Y position of this object.  Y is vertical, with 0,0 as the top left corner
    #----------------------------------------------------------------------
    
    #----------------------------------------------------------------------
    #Additional Functionality:
    
    
    #self.playerID()
      #Can be used to identify what player you are.

    #self.pirateCost()
      #Constant cost of a pirate unit

    #self.shipCost()
      #Constant cost of a ship unit

    #self.portCost()
      #Constant cost of a port

    #self.boardX()
      #The max length of the board's X

    #self.boardY()
      #The max length of the board's Y
      
    #self.getPath(startX, startY, endX, endY, tileType) 
      #Returns a vector of moves from the passed in start location to passed in end location over specified Tile type
      #0 = Land, 1 = Water. 
      #Example code provided in the snipets below
    #----------------------------------------------------------------------
  
    print "Turn:", self.turnNumber()
    print "My ID: ", self.playerID()
    print "My Gold: ", self.players[self.playerID()].getGold()

    #if you have enough gold to buy a pirate
    if self.pirateCost() < self.players[self.playerID()].getGold():
      #find a port you own
      for p in self.ports:
        if p.getOwner == self.playerID():
          p.createPirate()
          break

    #for each pirate in the world
    for i in self.pirates:
      #if I own the pirate
      if i.getOwner == self.playerID():
        #select a random pirate from the list
        target = random.choice(pirates)
        #Does a naive path finding algoritm that only takes into account tyle types, not other blocking problems
        #Takes a start x, start y, end x, end y, and a tile type on which you wish to path
        path = self.getPath(i.getX(), i.getY(), target.getX(), target.getY(), 0)
        #for all but the last step of the path, while I have steps, move
        for step in path:
          if i.getMovesLeft() <= 0:
            break
          i.move(step.getX(), step.getY())
        #get the distance between the guys
        distance = abs(i.getX() - target.getX()) + abs(i.getY() - target.getY())
        #If the distance is exactly 1 away and I don't own the guy
        if distance == 1 and i.getOwner() != target.getOwner():
          while i.getAttacksLeft() > 0:
           #attack the target
           i.attack(target)

    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
