#!/bin/env python
# -*- coding: iso-8859-1 -*-
# -*-python-*-

from library import library

from AI import AI

import sys

def main():
  if len(sys.argv) < 2:
    print "Please enter a host name."
    exit(1)
    
  connection = library.createConnection();
  
  ai = AI(connection)
    
  success = library.serverConnect(connection, sys.argv[1], "19000")
  if not success:
    sys.stderr.write("Unable to connect to server\n")
    exit(1)
  
  if not library.serverLogin(connection, ai.username(), ai.password()):
    exit(1)
  
  if len(sys.argv) < 3:
    library.createGame(connection)
  else:
    library.joinGame(connection, int(sys.argv[2]))
  while library.networkLoop(connection):
    if ai.startTurn():
      library.endTurn(connection)
    else:
      library.getStatus(connection)
  
  #Grab the end game state
  library.networkLoop(connection)
  #request the log file
  library.networkLoop(connection)

  ai.end()
  exit(0)


if __name__ == '__main__':
  main()
