//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that

#include <iostream>
#include <cstring>
#include <cstdlib>

#include "AI.h"
#include "network.h"
#include "game.h"

using namespace std;

int main(int argc, char** argv)
{

  if(argc < 2)
  {
    cout<<"Please enter a host name."<<endl;
    return 1;
  }

  Connection* c;
  c = createConnection();
  AI ai(c);
  int gameNumber;
  if(!serverConnect(c, argv[1], "19000"))
  {
    cerr << "Unable to connect to server" << endl;
    return 1;
  }
  if(!serverLogin(c, ai.username(), ai.password()))
  {
    return 1;
  }

  if(argc < 3)
  {
    gameNumber = createGame(c);
  }
  else
  {
    if(!joinGame(c, atoi(argv[2])))
    {
      cerr << "Error joining game." << endl;
      return 1;
    }
  }
  while(networkLoop(c))
  {
    if(ai.startTurn())
    {
      endTurn(c);
    }
    else
    {
      getStatus(c);
    }
  }
  ai.end();
  //Grab a log
  networkLoop(c);
  //Grab the end game status
  networkLoop(c);
  destroyConnection(c);
  return 0;
}

