# -*- coding: iso-8859-1 -*-
from base import *
from matchUtils import *
from objects import *
import networking.config.config
from collections import defaultdict
from networking.sexpr.sexpr import *
import os
import itertools
import scribe
import random
import customastar
from merchants import *

import traceback

Scribe = scribe.Scribe

def loadClassDefaults(cfgFile = "config/defaults.cfg"):
  cfg = networking.config.config.readConfig(cfgFile)
  for className in cfg.keys():
    for attr in cfg[className]:
      setattr(eval(className), attr, cfg[className][attr])

class Match(DefaultGameWorld):
  def __init__(self, id, controller):
    
    self.id = int(id)
    self.controller = controller
    DefaultGameWorld.__init__(self)
    self.scribe = Scribe(self.logPath())
    self.addPlayer(self.scribe, "spectator")

    #TODO: INITIALIZE THESE!
    self.turnNumber = -1
    self.playerID = -1
    self.gameNumber = id
    
    self.pirateHealth = 1
    self.pirateStrength = 1
    self.pirateSteps = 1
    self.pirateCost = 1
    self.pirateMoves = 1
    self.pirateAttacks = 1
    
    self.shipHealth = 1
    self.shipStrength = 1
    self.shipSteps = 1
    self.shipCost = 1
    self.shipRange = 1
    self.shipMoves = 1
    self.shipAttacks = 1
    
    self.portCost = 1
    
  def startMap(self, cfgUnits):
    map = [ [' ' for i in xrange(self.mapSize)] for j in xrange(self.mapSize)] 
    
    #open the map file for parsing
    
    #first we will look for all the .map files in the maps/ folder
    mapFilenames = []
    #look through entire maps directory
    for filename in os.listdir("maps/"):
      #and if the filename ends in .map
      if ".map" in filename:
        mapFilenames.append(filename)
    
    #now we can open the map by randomly choosing a filename in that list
    f = open(("maps/" + mapFilenames[random.randint(0,len(mapFilenames) - 1)]), 'r')
    
    encountered = set()
    
    #before we parse the map we will get the attributes for the Pirates, and Ships from the units.cfg file

    
    #now we actually parse the units.cfg file
    for i in cfgUnits.keys():
      if "pirate" in i.lower():
        self.pirateHealth = cfgUnits[i]["health"]
        self.pirateStrength = cfgUnits[i]["strength"]
        self.pirateSteps = cfgUnits[i]["steps"]
        self.pirateCost = cfgUnits[i]["cost"]
        self.pirateMoves = cfgUnits[i]["totalMoves"]
        self.pirateAttacks = cfgUnits[i]["totalAttacks"]
      elif "ship" in i.lower():
        self.shipHealth = cfgUnits[i]["health"]
        self.shipStrength = cfgUnits[i]["strength"]
        self.shipSteps = cfgUnits[i]["steps"]
        self.shipCost = cfgUnits[i]["cost"]
        self.shipRange = cfgUnits[i]["range"]
        self.shipMoves = cfgUnits[i]["totalMoves"]
        self.shipAttacks = cfgUnits[i]["totalAttacks"]
      elif "port" in i.lower():
        self.portCost = cfgUnits[i]["cost"]
    
    #this is where is parses through the map file and does tons of things!
    for y in range(0,self.mapSize):
      for x in range(0,self.mapSize):
        mapThing = f.read(1)
        #mapThing = text[x][y]
        if mapThing == ' ':
        #if the next byte is a ' ', it is nothing so read the next character
          mapThing = f.read(1)
          
        if mapThing == '\r':
        #if the next byte is a '\r' (carrier return) it is nothing so read the next character
          mapThing = f.read(1)
          
        if mapThing == '\n':
        #if the next byte is a '\n' (newline) it is nothing so read the next character
          mapThing = f.read(1)
          
        if mapThing == '.':
        #if the next byte is a '.' which is water
          #map[x][y] = 1
          self.addObject(Tile.make(self, x, y, 1))
        elif mapThing == 'X':
        #if the next byte is a 'X' which is land
          #map[x][y] = 0
          self.addObject(Tile.make(self, x, y, 0))
        elif mapThing == 'P':
        #if the next byte is a 'P' which is land with a player's port on top
          #map[x][y] = 0
          self.addObject(Tile.make(self, x, y, 0))
          if 'P' in encountered:
            self.addObject(Port.make(self, x, y, 1))
           
          else:
            encountered.add('P')
            self.addObject(Port.make(self, x, y, 0))
            
              
        else:
        #if the next byte is a '1' which is a neutral AI's 1st port with land below it
          #map[x][y] = 0
          self.addObject(Tile.make(self, x, y, 0))
          if mapThing in encountered:
            self.addObject(Port.make(self, x, y, 3))
            
            self.addObject(Treasure.make(self, x, y, self.npcStartingGold))  
            #for i in range(0,self.npcStartingPirates):
            #  self.addObject(Pirate.make(self, x, y, 3, self.pirateHealth, self.pirateStrength))
              
            #for i in range(0,self.npcStartingShips):
            #  self.addObject(Ship.make(self, x, y, 3, self.shipHealth, self.shipStrength))
              
          else:
            encountered.add(mapThing)
            self.addObject(Port.make(self, x, y, 2))
            
            self.addObject(Treasure.make(self, x, y, self.npcStartingGold))  
            #for i in range(0,self.npcStartingPirates):
            #  self.addObject(Pirate.make(self, x, y, 2, self.pirateHealth, self.pirateStrength))
              
            #for i in range(0,self.npcStartingShips):
            #  self.addObject(Ship.make(self, x, y, 2, self.shipHealth, self.shipStrength))

    for p in self.objects.ports:
      if (p.owner == 1 or p.owner == 0):
        for i in range(0,self.playersStartingPirates):
          self.addObject(Pirate.make(self, p.x, p.y, p.owner, self.pirateHealth, self.pirateStrength))
        
        #Finds empty water tiles, puts their locations in a list along with their modified distances from each player (modified such that one builds clockwise while the other builds counterclockwise)
        emptyWaterTiles = [[0,p.x,p.y]]
            
        for i in self.objects.tiles:
          if i.type == 1:
            empty = True
            for j in self.objects.ships:
              if j.x == i.x and j.y == i.y:
                empty = False
            if empty:
              emptyWaterTiles += [[modDistance(i,p),i.x,i.y]]
          if len(emptyWaterTiles) > self.playersStartingShips:
            break
        
        emptyWaterTiles.sort()
        for i in range(0,self.playersStartingShips):
          if len(emptyWaterTiles) >= 1:
            self.addObject(Ship.make(self, emptyWaterTiles[0][1], emptyWaterTiles[0][2], p.owner, self.shipHealth, self.shipStrength))
            emptyWaterTiles.pop(0)
    
    #for y in range(0,self.mapSize):
      #print "\n",
      #for x in range(0,self.mapSize):
        #print (map[x][y]),
        #self.addObject(Tile.make(self, x, y, map[x][y]))
    self.Merchant2 = MerchantAI(self,2)
    self.Merchant3 = MerchantAI(self,3)
    
  def startTreasures(self):
    #temp code that makes 2 treasures
    i = 1
    #self.addObject(Treasure.make(self, 2, 8, -1, 100))
    #self.addObject(Treasure.make(self, 8, 2, -1, 100))

  def addPlayer(self, connection, type="player"):
    connection.type = type
    if len(self.players) >= 2 and type == "player":
      return "Game is full"
    if type == "player":
      self.players.append(connection)
    elif type == "spectator":
      self.spectators.append(connection)
      #If the game has already started, send them the ident message
      if (self.turn is not None):
        self.sendIdent([connection])
    return True

  def removePlayer(self, connection):
    #traceback.print_stack()
    if connection in self.players:
      if self.turn is not None:
        winner = self.players[1 - self.getPlayerIndex(connection)]
        self.declareWinner(winner)
        if 1 - self.getPlayerIndex(connection) == 1:
          print "1 Wins!"
        else:
          print "2 Wins!"
      self.players.remove(connection)
    else:
      self.spectators.remove(connection)

  def start(self):
    if len(self.players) < 2:
      return "Game is not full"
    if self.winner is not None or self.turn is not None:
      return "Game has already begun"
    
    #TODO: START STUFF

    self.turnNumber = -1
    #creates the players data
    for i in self.players:
      self.addObject(Player.make(self,i.screenName,self.playersStartingGold,self.startTime))
    
    cfgUnits = networking.config.config.readConfig("config/units.cfg")
    self.startMap(cfgUnits)
    self.startTreasures()
    #print self.objects.values()
    #print [i for i in self.objects.values() if isinstance(i,Player)]
    
    self.sendIdent(self.players + self.spectators)

    self.turn = self.players[1]

    self.nextTurn()
    print "Starting game " + `self.id`
    return True


  def nextTurn(self):
    self.turnNumber += 1
    if self.turn == self.players[0]:
      self.turn = self.players[1]
      self.playerID = 2
      for obj in self.objects.values():
        obj.nextTurn()
      self.Merchant2.play()
      self.playerID = 1
    elif self.turn == self.players[1]:
      self.turn = self.players[0]
      self.playerID = 3
      for obj in self.objects.values():
        obj.nextTurn()
      self.Merchant3.play()
      self.playerID = 0

    else:
      return "Game is over."
    
    #here is how a star works
    #this goes over water from (0,0) to (39,39) return a list of directions to move to get there
    #route = customastar.aStar(self, 1, 0, 0, 39, 39)
    #print route
    
    for obj in self.objects.values():
      obj.nextTurn()

    self.checkWinner()
    if self.winner is None:
      self.sendStatus([self.turn] +  self.spectators)
    else:
      self.sendStatus(self.spectators)
    self.animations = ["animations"]
    return True

  def checkWinner(self):
    #TODO: Make this check if a player won, and call declareWinner with a player if they did
    firstFound = False
    player1 = Player
    player2 = Player
    for i in self.objects.players:
      if firstFound == False:
        player1 = i
        firstFound = True
      else:
        player2 = i
    if self.turnNumber >= self.turnLimit:
      #Check for victory through wealth
      if player2.gold > player1.gold:
        self.declareWinner(self.players[1], 'Victory Through Wealth!')
        print "2 Wins!"
      elif player1.gold > player2.gold:
        self.declareWinner(self.players[0], 'Victory Through Wealth!')
        print "1 Wins!"
      elif player1.gold == player2.gold:
      #currently living ships * ship cost + currently living pirates * pirate cost + ports * portCost
      #Victory through strength
        player1Total = 0
        player2Total = 0
        for i in self.objects.ships:
          if i.owner == 0:
            player1Total += self.shipCost
          elif i.owner == 1:
            player2Total += self.shipCost
        for i in self.objects.pirates:
          if i.owner == 0:
            player1Total += self.pirateCost
          elif i.owner == 1:
            player2Total += self.pirateCost
        for i in self.objects.ports:
          if i.owner == 0:
            player1Total += self.portCost
          elif i.owner == 1:
            player2Total += self.portCost
        if player1Total > player2Total:
          self.declareWinner(self.players[0], 'Victory Through Strength!')
          print "1 Wins!"
        elif player1Total < player2Total:
          self.declareWinner(self.players[1], 'Victory Through Strength!')
          print "2 Wins!"
        elif player1Total == player2Total:
          #Victory Through Hardiness
          player1Total = 0
          player2Total = 0
          for i in self.objects.ships:
              if i.owner == 0:
                player1Total += i.health
              elif i.owner == 1:
                player2Total += i.health
          for i in self.objects.pirates:
            if i.owner == 0:
              player1Total += i.health
            elif i.owner == 1:
              player2Total += i.health
          if player1Total > player2Total:
            self.declareWinner(self.players[0], 'Victory Through Hardiness!')
            print "1 Wins!"
          elif player1Total < player2Total:
            self.declareWinner(self.players[1], 'Victory Through Hardiness!')
            print "2 Wins!"
          elif player1Total == player2Total: 
            self.declareWinner(self.players[1], 'The Match is a Draw!')  
            print "Tie game!"          
    #Victory through annihilation
    #Checks to see if opponent has less gold than that required to buy a pirate first    
    elif player1.gold < self.pirateCost or player2.gold < self.pirateCost:
      player1Loss = False
      player2Loss = False
      if player1.gold < self.pirateCost:
        player1Loss = True
      if player2.gold < self.pirateCost:
        player2Loss = True
      #This checks to see if they have any pirates
      for i in self.objects.pirates:
        if i.owner == 0:              
          player1Loss = False
        elif i.owner == 1:
          player2Loss = False
         
      #If a player has less gold than required for a pirate
      if player1Loss == True or player2Loss == True:   
        #print "In loss loop"
        #print player1Loss       
        #print player2Loss 
        #print player1.gold        
        #print player2.gold  
        if player1Loss == True and player2Loss == False:
          self.declareWinner(self.players[1], 'Victory Through Annihilation')
          print "2 Wins!"         
        elif player1Loss == False and player2Loss == True:
          self.declareWinner(self.players[0], 'Victory Through Annihilation')
          print "1 Wins!"
        elif player1Loss == True and player2Loss == True and player1.gold < player2.gold:
          self.declareWinner(self.players[1], 'Victory Through Annihilation') 
          print "2 Wins!"
        elif player2Loss == True and player1Loss == True and player2.gold < player1.gold:
          self.declareWinner(self.players[0], 'Victory Through Annihilation') 
          print "1 Wins!"
        elif player1Loss == True and player2Loss == True and player1.gold == player2.gold:
          self.declareWinner(self.players[1], 'The Match is a Draw')    
          print "Tie game!"              
    return

  def declareWinner(self, winner, reason=''):
    self.winner = winner

    msg = ["game-winner", self.id, self.winner.user, self.getPlayerIndex(self.winner), reason]
    self.scribe.writeSExpr(msg)
    self.scribe.finalize()
    self.removePlayer(self.scribe)

    for p in self.players + self.spectators:
      p.writeSExpr(msg)

    self.sendStatus([self.turn])
    self.playerID ^= 1
    self.sendStatus([self.players[self.playerID]])
    self.playerID ^= 1
    self.turn = None
    
  def logPath(self):
    return "logs/" + str(self.id) + ".gamelog"

  @derefArgs(Unit, None, None)
  def move(self, object, x, y):
    return object.move(x, y, )

  @derefArgs(Unit, None)
  def talk(self, object, message):
    return object.talk(message, )

  @derefArgs(Unit, Unit)
  def attack(self, object, Target):
    return object.attack(Target, )

  @derefArgs(Pirate, None)
  def pickupTreasure(self, object, amount):
    return object.pickupTreasure(amount, )

  @derefArgs(Pirate, None)
  def dropTreasure(self, object, amount):
    return object.dropTreasure(amount, )

  @derefArgs(Pirate)
  def buildPort(self, object):
    return object.buildPort()

  @derefArgs(Port)
  def createPirate(self, object):
    return object.createPirate()

  @derefArgs(Port)
  def createShip(self, object):
    return object.createShip()


  def sendIdent(self, players):
    if len(self.players) < 2:
      return False
    list = []
    for i in itertools.chain(self.players, self.spectators):
      list += [[self.getPlayerIndex(i), i.user, i.screenName, i.type]]
    for i in players:
      i.writeSExpr(['ident', list, self.id, self.getPlayerIndex(i)])

  def getPlayerIndex(self, player):
    try:
      playerIndex = self.players.index(player)
    except ValueError:
      playerIndex = -1
    return playerIndex

  def sendStatus(self, players):
    for i in players:
      i.writeSExpr(self.status())
      i.writeSExpr(self.animations)
    return True


  def status(self):
    msg = ["status"]

    msg.append(["game", self.turnNumber, self.playerID, self.gameNumber, self.pirateCost, self.shipCost, self.portCost, self.mapSize])

    typeLists = []
    typeLists.append(["Pirate"] + [i.toList() for i in self.objects.values() if i.__class__ is Pirate])
    typeLists.append(["Player"] + [i.toList() for i in self.objects.values() if i.__class__ is Player])
    typeLists.append(["Port"] + [i.toList() for i in self.objects.values() if i.__class__ is Port])
    typeLists.append(["Ship"] + [i.toList() for i in self.objects.values() if i.__class__ is Ship])
    if self.turnNumber < 4:
      typeLists.append(["Tile"] + [i.toList() for i in self.objects.values() if i.__class__ is Tile])
    typeLists.append(["Treasure"] + [i.toList() for i in self.objects.values() if i.__class__ is Treasure])

    msg.extend(typeLists)

    return msg

#returns a value that when sorted will result in a counterclockwise or clockwise sort order
def modDistance(tile,port):
  runningTotal = 0.0
  runningTotal += 10000*(abs(port.x-tile.x) + abs(port.y-tile.y))
  if port.owner == 0:
    if port.y > tile.y:
      runningTotal += .0001*(port.x-tile.x)
    elif port.y == tile.y:
      if port.x > tile.x:
        runningTotal += 1
      else:
        runningTotal += 1000
    elif port.y < tile.y:
      runningTotal += 100+(tile.x-port.x)
      
  if port.owner == 1:
    if port.y < tile.y:
      runningTotal += .0001*(tile.x-port.x)
    elif port.y == tile.y:
      if port.x < tile.x:
        runningTotal += 1
      else:
        runningTotal += 1000
    elif port.y > tile.y:
      runningTotal += 100+(port.x-tile.x)      
  
  return runningTotal
  

loadClassDefaults()

