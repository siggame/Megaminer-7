# -*- coding: iso-8859-1 -*-
#from merchants import *
from math import sqrt
class Mappable:
  def __init__(self, game, id, x, y):
    self.game = game
    self.id = id
    self.x = x
    self.y = y

  def toList(self):
    value = [
      self.id,
      self.x,
      self.y,
      ]
    return value

  def nextTurn(self):
    pass



class Unit(Mappable):
  def __init__(self, game, id, x, y, owner, health, strength, movesLeft, attacksLeft, gold):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.health = health
    self.strength = strength
    self.movesLeft = movesLeft
    self.attacksLeft = attacksLeft
    self.gold = gold

  def toList(self):
    value = [
      self.id,
      self.x,
      self.y,
      self.owner,
      self.health,
      self.strength,
      self.movesLeft,
      self.attacksLeft,
      self.gold,
      ]
    return value

  def nextTurn(self):
    pass

  def move(self, x, y):
    print "Wrong move"
    return True

  def talk(self, message):
    self.game.animations.append(['talk', self.id, message])
    return true

  def attack(self, Target):
    pass
  
  def _distance(self, x, y):
    distance = abs(self.x-x)+abs(self.y-y)
    return distance

  def _takeDamage(self, damage):
    self.health -= damage
    if self.health < 1 and self.id in self.game.objects:
      self.game.removeObject(self)



class Pirate(Unit):
  def __init__(self, game, id, x, y, owner, health, strength, movesLeft, attacksLeft, gold):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.health = health
    self.strength = strength
    self.movesLeft = movesLeft
    self.attacksLeft = attacksLeft
    self.gold = gold

  def toList(self):
    value = [
      self.id,
      self.x,
      self.y,
      self.owner,
      self.health,
      self.strength,
      self.movesLeft,
      self.attacksLeft,
      self.gold,
      ]
    return value

  @staticmethod
  def make(game, x, y, owner, health, strength):
    id = game.nextid
    game.nextid += 1
    # Placeholder for health and strength as 1, 1 respectively
    return Pirate(game, id, x, y, owner, health, strength, 0, 0, 0)

  def nextTurn(self):
    if self.game.playerID != self.owner:
      self.movesLeft = 0
      self.attacksLeft = 0
      return True
    else:  
      self.movesLeft = self.game.pirateMoves
      self.attacksLeft = self.game.pirateAttacks
    pass
    
  def takeDamage(self, pirate):
    self.health -= pirate.strength
    #Merchants add attacker to shitlist
    if self.owner == 2 or self.owner == 3: 
      found = False
      if pirate not in self.traderGroup.shitlist:
        self.traderGroup.shitlist += [pirate]
    #If pirate is killed by the attack
    if self.health <= 0:
      #If the pirate did not kill himself, transfer gold to killing pirate... if it was a pirate that killed him
      if pirate.id != self.id and isinstance(pirate,Pirate):
        pirate.gold += self.gold
      #Otherwise the treasure becomes free game, or falls in your port, whichever
      
      else:
        if self.gold > 0:
          self.reallyDropTreasure(self.gold)
      if self.owner == 2:
        self.game.Merchant2.pirateDied(self)
      if self.owner == 3:
        self.game.Merchant3.pirateDied(self)
    
        #Lose control of ship if this is your last pirate leaving
      for i in self.game.objects.ships:
        if i.x == self.x and i.y == self.y:
          if i.owner == self.owner:
            counter = 0
            #if the pirate was on a ship, count how many pirates are on it
            for j in self.game.objects.pirates:
              if j.x == i.x and j.y == i.y:
                counter+=1
                if counter > 1:
                  break
            #If this was the last pirate on board, the ship becomes neutral.
            if counter == 1:
              if i.owner == 2:
                self.game.Merchant2.shipLost(i)
              if i.owner == 3:
                self.game.Merchant3.shipLost(i)
              i.owner = -1
          break
      self.game.removeObject(self)

    return True
          
      

  def move(self, x, y):
    #Checking to see if moving a valid piece
    if self.owner != self.game.playerID:
      return "Ye can't move a unit that doesn't belong to you, argghh"  
 
    #Checks to see if the unit has moved this turn
    #0 if has not moved
    if self.movesLeft <= 0:
      return "That unit has alrrready moved this terrn"
    
    #Makes sure the unit is only moving one space
    if self._distance(x,y) > 1:
      return "Ye cannot move that farr"  
   
    elif self._distance(x,y) == 0:
      return "Ye already be at that location, matey"  

    #Checking to make sure the unit is in the bounds of the map
    if x > self.game.mapSize -1:
      return "Stepping off the world, the kracken shall get ye"
    elif y > self.game.mapSize -1:
      return "Stepping off the world, the kracken shall get ye"
    elif y < 0:
      return "Stepping off the world, the kracken shall get ye"
    elif x < 0:
      return "Stepping off the world, the kracken shall get ye"

    freeShip = False
    intoWater = False
    theFreeShip = None
    #Check to see if the unit is moving into an enemy
    for i in self.game.objects.pirates:
      if i.owner != -1 and i.owner != self.owner and i.x == x and i.y == y:
        return "Therr already be an enemy at that location, yarr"
        
    for i in self.game.objects.ships:
      if i.owner != -1 and i.owner != self.owner and i.x == x and i.y == y:
        return "Therr already be an enemy at that location, yarr"
      elif (i.owner == self.owner or i.owner == -1) and i.x == x and i.y == y:
        freeShip = True
        theFreeShip = i
        break
    for i in self.game.objects.ports:
      #Check to see if the unit is moving into an enemy port
      if i.owner != self.owner and i.x == x and i.y == y: 
        return "Ye cannot move yerr pirates into enemy ports"
    for i in self.game.objects.tiles:
      #Checking if unit is moving onto water
      if i.x == x and i.y == y and i.type == 1:
        intoWater = True      
    if intoWater and not freeShip:
      return "Yer pirates cannot enter water without a boat"
    #Point of no return
    #take control of a ship if you move onto it
    if freeShip and theFreeShip is not None:
      theFreeShip.owner = self.owner
    #Lose control of ship if this is your last pirate leaving
    counter = 0
    onABoat = False
    theBoatIAmOn = None
    for i in self.game.objects.ships: 
      if i.x == self.x and i.y == self.y:
        onABoat = True
        theBoatIAmOn = i
        break
        #if the pirate was on a ship, count how many pirates are on
    counter = 0
    if onABoat:
      for i in self.game.objects.pirates:
        if x == i.x and y == i.y:
          counter+=1
            #If this was the last pirate on board, the ship becomes neutral.
          if counter > 1:
            break
    if onABoat and counter == 1:
      theBoatIAmOn.owner = -1
            
    #Moves the unit and makes it unable to move until next turn
    self.game.animations.append(['move', self.id,x,y])
    self.movesLeft -= 1
    self.x = x
    self.y = y
    
    return True

  def talk(self, message):
    self.game.animations.append(['talk', self.id, message])
    return True

  def pickupTreasure(self, amount):
    if self.owner != self.game.playerID:
      return "Ye cannot make me pickup that therr treasurrr. Ye be not my captain!"  
    #If trying to use pickup treasure and standing on a port  
    portPickup = False
    for i in self.game.objects.ports:       
      if i.x == self.x and i.y == self.y and (self.owner == 0 or self.owner == 1):
        print "On a port"
        portPickup = True
        break
    if amount < 1:
      return "We be not interested in picking up such small amounts of gold!"
    if portPickup == True:
      #Checks to make sure amount being withdrawn is less than that player has
      if amount <= self.game.objects.players[self.owner].gold:
        self.gold += amount
        self.game.objects.players[self.owner].gold -= amount
        return True
      else:
        return "Ye do not have that much gold, yargh!"
              
    #If the pirate is not on a port and is trying to pickup Treasure
    if portPickup == False:
      for i in self.game.objects.treasures:
          if i.x == self.x and i.y == self.y:
            #Check to make sure the amount being picked up isn't greater than its value
            if amount > i.gold:
              return "Ye do not have that much gold!"
            elif amount < 1:
              return "Ye have to pick up somethin!"
            #Checks to see if the pirate has treasure
            if amount == i.gold:
              self.gold += amount
              self.game.removeObject(i)
              return True
            elif amount < i.gold:
              i.gold -= amount
              self.gold += amount
            return True               
      for i in self.game.objects.ships:
        if i.x == self.x and i.y == self.y:
          if amount > i.gold:
            return "Yer boat does not have that much gold!"
          elif amount < 1:
            return "Ye have to pick up somethin!"
          i.gold -= amount
          self.gold += amount
          return True
      return "Thar be no treasure for me to pick up!"
    return True
  
  def dropTreasure(self, amount):
    if self.owner != self.game.playerID:
      return "Yarr!  Ye cannot trick me into dropin' me treasure!  Yer not me captain!" 
    return self.reallyDropTreasure(amount)
  
  #added this so I can call the drop treasure function without it checking wether or not it is that unit's turn, should make the killing of oneself easier.
  def reallyDropTreasure(self,amount):
    if amount > self.gold:
      return "Yarrgh, I don't have that much gold!"
    if amount < 1:
      return "Droppin' no gold be useless!"
    for j in self.game.objects.ports:
      #if the treasure is being dropped on a port
      if (j.owner == 0 or j.owner == 1):
        if self.x == j.x and self.y == j.y:
          #Increase gold of owner
          if self.owner == 0:
            self.game.objects.players[0].gold += amount
          else:
            self.game.objects.players[1].gold += amount
          #Decrement gold if only partially dropped
          self.gold -= amount
          return True
    for j in self.game.objects.treasures:    
      if self.x == j.x and self.y == j.y:
        j.gold += amount
        self.gold -= amount
        return True
    for j in self.game.objects.ships:
      if self.x == j.x and self.y == j.y:
        j.gold += amount
        self.gold -= amount
        return True
    self.game.addObject(Treasure.make(self.game,self.x,self.y,amount))
    self.gold -= amount
    return True
                      
  def buildPort(self):
    if self.owner != self.game.playerID:
      return "Yarr, ye can't make me build a port! Ye are not my captain!"  
    #checks for distance to nearest port
    for i in self.game.objects.ports:
      if self._distance(i.x,i.y) < 3:
        return "This port be too close to another port!"
    nearWater = False
    onLand = False
    for i in self.game.objects.tiles:
      if i._distance(self.x,self.y) == 1 and i.type == 1: #Not sure about this
        nearWater = True
      if i._distance(self.x,self.y) == 0 and i.type == 0:
        onLand = True
    if not nearWater:
      return "Our ports must be near water!"
    if not onLand:
      return "Ports must be built on land"
    
    if self.owner == 0:
      if self.game.objects.players[0].gold >= self.game.portCost:
        #Checks to see if there is treasure on the loaction of the new port
        for j in self.game.objects.treasures:
          if j.x == self.x and j.y == self.y:
            self.game.objects.players[0].gold += j.gold
            self.game.removeObject(j)
        self.game.objects.players[0].gold -= self.game.portCost
        port = Port.make(self.game,self.x,self.y,self.owner)
        self.game.addObject(port)
        return True
      else:
        return "We do not have enough gowld to make tha' port, captain!"
    else:
      if self.game.objects.players[1].gold >= self.game.portCost:
        #Checks to see if there is treasure on the loaction of the new port
        for j in self.game.objects.treasures:
          if j.x == self.x and j.y == self.y:
            self.game.objects.players[1].gold += j.gold
            self.game.removeObject(j)
        self.game.objects.players[1].gold -= self.game.portCost
        port = Port.make(self.game,self.x,self.y,self.owner)
        self.game.addObject(port)
        return True
      else:
        return "We do not have enough gowld to make tha' port, captain!"
 
    return True
  #TODO: Test and review this logic

  def attack(self, Target):
    #Ensures that you own the attacking unit
    if Target not in self.game.objects.pirates:
      return "That Target does not exist"
    if self.owner != self.game.playerID:
      return "I do not take orders from you! You be not my captain"
      
    elif not isinstance(Target,Pirate):
      return "That unit cannot be attacked, captain!"
    
    elif self.attacksLeft <= 0:
      return "Yee've already attacked this turn!"
    
    elif not (abs(self.x - Target.x)+abs(self.y  - Target.y) <= 1):
      return "That be too farr away!"
    
    else:
      self.attacksLeft -= 1
      #Optional Ally Pirate Auto Kill
      if Target.owner is self.owner:
        Target.health = 0
      self.game.animations.append(['PirateAttack', self.id,Target.x,Target.y])
      Target.takeDamage(self)
      return True




class Player:
  def __init__(self, game, id, playerName, gold, time):
    self.game = game
    self.id = id
    self.playerName = playerName
    self.gold = gold
    self.time = time

  def toList(self):
    value = [
      self.id,
      self.playerName,
      self.gold,
      self.time,
      ]
    return value

  def nextTurn(self):
    pass
  
  @staticmethod
  def make(game, playerName, gold, time):
    id = game.nextid
    game.nextid += 1
    return Player(game, id, playerName, gold, time)

class Port(Mappable):
  def __init__(self, game, id, x, y, owner):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner

  def toList(self):
    value = [
      self.id,
      self.x,
      self.y,
      self.owner,
      ]
    return value

  @staticmethod
  def make(game, x, y, owner):
    id = game.nextid
    game.nextid += 1
    return Port(game, id, x, y, owner)
    
  def nextTurn(self):
    pass
    

  def createPirate(self):
    if self.owner != self.game.playerID:
      return "That be not your port!"
    #Decrememnting gold of corresponding player
    if self.owner == 0:
      if self.game.objects.players[0].gold >= self.game.pirateCost:
        self.game.objects.players[0].gold -= self.game.pirateCost
      else:
        return "We don' have enough gold fer that unit, captain"
    else:
      if self.game.objects.players[1].gold >= self.game.pirateCost:
        self.game.objects.players[1].gold -= self.game.pirateCost
      else:
        return "We don' have enough gold fer that unit, captain"
    pirate = Pirate.make(self.game, self.x, self.y, self.owner, self.game.pirateHealth, self.game.pirateStrength) #placeholder values
    self.game.addObject(pirate)
    for s in self.game.objects.ships:
        if s.x == self.x and s.y == self.y:
          if s.owner == -1:
            s.owner = self.owner
    return True
  #TODO: Test and review this logic

  def createShip(self):
    if self.owner != self.game.playerID:
      return "That be not your port!"
    #Decrememnting gold of corresponding player
    if self.owner == 0:
      if self.game.objects.players[0].gold >= self.game.shipCost:
        self.game.objects.players[0].gold -= self.game.shipCost
      else:
        return "We don' have enough gold fer that unit, captain"
    else:
      if self.game.objects.players[1].gold >= self.game.shipCost:
        self.game.objects.players[1].gold -= self.game.shipCost
      else:
        return "We don' have enough gold fer that unit, captain"
    #Checks to make sure there is no other ships in the port
    for i in self.game.objects.ships:
      if i.x == self.x and i.y == self.y:
        return "Therr already be a ship in that port, cap'n"
    havePirateHere = False
    for i in self.game.objects.pirates:
      if i.x == self.x and i.y == self.y:
        havePirateHere = True
        ship = Ship.make(self.game, self.x, self.y, self.owner, self.game.shipHealth, self.game.shipStrength) #placeholder values
        self.game.addObject(ship)
        break
    if not havePirateHere:
      ship = Ship.make(self.game, self.x, self.y, -1, self.game.shipHealth, self.game.shipStrength) #placeholder values
      self.game.addObject(ship)
    return True    
    pass



class Ship(Unit):
  def __init__(self, game, id, x, y, owner, health, strength, movesLeft, attacksLeft, gold):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.health = health
    self.strength = strength
    self.movesLeft = movesLeft
    self.attacksLeft = attacksLeft
    self.gold = gold

  def toList(self):
    value = [
      self.id,
      self.x,
      self.y,
      self.owner,
      self.health,
      self.strength,
      self.movesLeft,
      self.attacksLeft,
      self.gold,
      ]
    return value

  @staticmethod
  def make(game, x, y, owner, health, strength):
    id = game.nextid
    game.nextid += 1
    # Placeholder for health and strength as 1, 1 respectively
    return Ship(game, id, x, y, owner, health, strength, 0, 0, 0)

  def nextTurn(self): 
    self.movesLeft = self.game.shipMoves
    self.attacksLeft = self.game.shipAttacks
    for p in self.game.objects.pirates:
      if p.x == self.x and p.y == self.y:
        self.owner = p.owner
        #brea

  def move(self, x, y):
    #Check the owner of the ship before moving
    if self.owner != self.game.playerID:
      return "This be not yarr ship, ye swine!"
      
    if self.movesLeft <= 0:
      return "This ship has alrready used all of its moves this turrn" 
     
    if self._distance(x,y) > 1:
      return "The ship cannot move that far, captain!"
   
    elif self._distance(x,y) == 0:
      return "The ship is already at that location, captain!"
    
    #Checking the bounds of the map
    if x > self.game.mapSize -1:
      return "Stepping off the world, the kracken lies beyond!"
    elif y > self.game.mapSize -1:
      return "Stepping off the world, the kracken lies beyond!"
    elif y < 0:
      return "Stepping off the world, the kracken lies beyond!"
    elif x < 0:
      return "Stepping off the world, the kracken lies beyond!" 
     
    #Makes sure the ship stays on water
    isWater = True
    portTile = False
    i = self.game.objects.tiles[x + y * self.game.mapSize]
    #If the ship is attempting to move onto a land tile
    if i.type != 1:
      #This variable checks whether or not the ship is trying to move onto a port
      isWater = False
    for i in self.game.objects.ports:
      if i.x == x and i.y == y:
        #True if we find a port at desired location
        portTile = True
        #If the port does not belong to you, throw an error
        if i.owner != self.game.playerID and not ((self.game.playerID == 2  or self.game.playerID == 3) and (i.owner == 2 or i.owner == 3)):
          return "We cannot move arr ships into enemy ports!"  
        if self.owner < 2:   
          self.game.objects.players[self.owner].gold += self.gold
          self.gold = 0             
        break
    #Makes sure there is no units at target location
    for i in self.game.objects.ships: 
      if i.x == x and i.y == y:
        return "Therr already be a ship at that location!" 
    #If the player is simply trying to move a ship onto land
    if portTile == False and isWater == False:
      return "Ships cannot move onto land, captain!"
      
    #Ship has passed all checks and it ready to move
    self.movesLeft -= 1
    
    #Moving all treasure,pirates on the ship to the new location
    #Also moves the ship to the new location
    for i in self.game.objects.pirates:
      if i.x == self.x and i.y == self.y:
        i.x = x
        i.y = y
        
    self.x = x
    self.y = y
       
    return True
    
  def talk(self, message):
    pass

  def attack(self, Target):
    #Make sure you own the attacking unit
    if self.owner != self.game.playerID:
      return "This be not yarr ship, ye swine!"
    if Target not in self.game.objects.ships:
      return "Ye may only attack enemy ships with arr ships"
    #Checks to see that the target is in range     
    if self._distance(Target.x,Target.y) > self.game.shipRange:
      return "That tarrget is out of arr range, sir!"      
      
    #Meets all conditions for attack
    if self.attacksLeft <= 0:
      return "Our ship be out of cannon balls for the terrrn. We must reload, captain!"
    self.attacksLeft -= 1   
    self.game.animations.append(['ShipAttack', self.id,Target.x,Target.y])
    Target.takeDamage(self)
    return True
    
  def takeDamage(self, attacker):
    self.health -= attacker.strength
    if self.owner is 2 or self.owner is 3:
      found = False
      for enemy in self.traderGroup.shitlist:
        if enemy is attacker:
          found = True
          break
      if not found:
        self.traderGroup.shitlist += [attacker]
    #If the ship is killed by the attack
    #Destroy everything that was on it
    #If it was not at a port
    if self.health <= 0:
      atPort = False
      for i in self.game.objects.ports:
        if i.x == self.x and i.y == self.y:
          atPort = True
      if not atPort:
        for i in self.game.objects.pirates:
          if i.x == self.x and i.y == self.y: 
            if i.owner == 2:
              self.game.Merchant2.pirateDied(i)
            if i.owner == 3:
              self.game.Merchant3.pirateDied(i)
            self.game.removeObject(i)
      self.game.removeObject(self)
    return True          

class Tile(Mappable):
  def __init__(self, game, id, x, y, type):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.type = type

  def toList(self):
    value = [
      self.id,
      self.x,
      self.y,
      self.type,
      ]
    return value

  def _distance(self, x, y):
    distance = 0
    if self.x > x:
      distance += self.x - x
    elif  x > self.x:
      distance += x - self.x
    if self.y > y:
      distance += self.y - y
    elif y > self.y:
      distance += y - self.y
    return distance

  @staticmethod
  def make(game, x, y, type):
    id = game.nextid
    game.nextid += 1
    #1 is water, 0 is land
    return Tile(game, id, x, y, type)
  
  def nextTurn(self):
    pass



class Treasure(Mappable):
  def __init__(self, game, id, x, y, gold):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.gold = gold

  def toList(self):
    value = [
      self.id,
      self.x,
      self.y,
      self.gold,
      ]
    return value

  @staticmethod
  def make(game, x, y, gold):
    id = game.nextid
    game.nextid += 1
    return Treasure(game, id, x, y, gold)
  
  def nextTurn(self):
    closest = self.game.mapSize*2
    for p in self.game.objects.pirates:
      if p._distance(self.x,self.y) < closest:
        closest = p._distance(self.x,self.y)
    self.gold += int(sqrt(closest))
