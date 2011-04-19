import com.sun.jna.Pointer;

import java.util.Random;

///The class implementing gameplay logic.
class AI extends BaseAI
{
  Random rand;
  
  //NOTE: You must change the return value of this to the username you team sets on MegaMinerAI.com
  public String username()
  {
    return "Shell AI";
  }
  
  //NOTE: You must change the return value of this to the password you team sets on MegaMinerAI.com
  public String password()
  {
    return "password";
  }
  
  //////////////////////////////////////////////
  //Pre-Defined Data Structures : 
  //Pirate[] pirates
  //Ship[] ships
  //Port[] ports
  //Tile[] tiles
  //Treasure[] treasures
  ///////////////////////////////////////////// 
  //If you are a cs53 student and don't know what an array is or how to use it
  //please find a Dev and we will help you! 
  /////////////////////////////////////////////////////////////////
  
  /////////////////////////////////////////////////////////////////
  //Port Functions:  
  
  //ports[i].id()
    ///Unique Identifier

  //ports[i].x()
    ///The X position of this object.  X is horizontal, with 0,0 as the top left corner

  //ports[i].y()
    ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner

  //ports[i].owner()
    ///The owner of the port
    
  //ports[i].createPirate()
    ///creates a pirate at the calling port
      
  //ports[i].createShip()
    ///creates a ship at the calling port
  ///////////////////////////////////////////////////////////////////
  
    ///////////////////////////////////////////////////////////////////
  //Pirate/Ship Functions:
  
  //pirates[i].id() / ships[i].id()
    ///Unique Identifier
    
  //pirates[i].x() / ships[i].x()
    ///The X position of this object.  X is horizontal, with 0,0 as the top left corner

  //pirates[i].y() / ships[i].y()
    ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner

  //pirates[i].owner() / ships[i].owner()
    ///The owner of the unit

  //pirates[i].health() / ships[i].health()
    ///health of the unit

  //pirates[i].strength() / ships[i].strength()
    ///attacking strength of the unit

  //pirates[i].movesLeft() / ships[i].movesLeft()
    ///Attacks left this turn for the unit

  //pirates[i]/attacksLeft() / ships[i].attacksLeft()
    ///Moves left this turn for the unit

  //pirates[i].gold() / ships[i].gold()
    ///Amoutn of gold the unit is carrying
    
  //pirates[i].attack( Pirate target) / ships[i].attacks(Ship target)
    ///Attacks the passed in unit if possible
      
  //pirates[i].move(int x,int y) / ships[i].move(int x, int y)
    ///Moves to the passed in location if possible
    
  //pirates[i].createPort() (ONLY FOR PIRATES)
    ///Creates a port at the pirate's current location if possible 
    
  //pirates[i].pickupTreasure(int goldAmount) (ONLY FOR PIRATES)
    ///Picks up gold from the ground or from a port
  
  //pirates[i].dropTreasure(int goldAmount) (ONLY FOR PIRATES)
    ///Pirate drops its gold
  ///////////////////////////////////////////////////////////////////
  
  ///////////////////////////////////////////////////////////////////
  //Tile Functions:
  
  //tiles[i].id()
    ///Unique Identifier

  //tiles[i].x()
    ///The X position of this object.  X is horizontal, with 0,0 as the top left corner

  //tiles[i].y()
    ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner

  //tiles[i].type()
    ///land = 0, water = 1
  ///////////////////////////////////////////////////////////////////

  ///////////////////////////////////////////////////////////////////
  //Treasure Functions:
  
  //treasures[i].id()
    ///Unique Identifier

  //treasures[i].x()
    ///The X position of this object.  X is horizontal, with 0,0 as the top left corner

  //treasures[i].y()
    ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  ///////////////////////////////////////////////////////////////////
  
  ///////////////////////////////////////////////////////////////////
  //Additional Functionality:

  //playerID()
    ///Can be used to identify what player you are.

  //PirateCost()
    ///Constant cost of a pirate unit

  //ShipCost()
    ///Constant cost of a ship unit

  //PortCost()
    ///Constant cost of a port

  //boardX()
    ///The max length of the board's X

  //boardY()
    ///The max length of the board's Y

  //getPath(int startX, int startY, int endX, int endY, int tileType) 
    ///Returns a vector of moves from the passed in start location to passed in end location over specified Tile type
    ///0 = Land, 1 = Water. 
    ///Example code provided in the snipets below
  ///////////////////////////////////////////////////////////////////
  
  //This function is called each time it is your turn
  //Return true to end your turn, return false to ask the server for updated information
  public boolean run()
  {
    System.out.println("Turn: " + turnNumber() + " My ID: " + playerID() + " My Gold: " + players[playerID()].getGold() + "\n");

    // if you have enough gold to buy a pirate
    if(pirateCost() < players[playerID()].getGold())
    {
      // find a port that you own
      for(int p=0;p<ports.length;p++)
      {
        if(ports[p].getOwner()==playerID())
        {
          ports[p].createPirate();
          break;
        }
      }
    }

    // For each pirate in the world
    for(int i=0;i<pirates.length;i++)
    {
      // if I own the pirate
      if(pirates[i].getOwner()==playerID())
      {
        // select a random pirate from the list
        int target = rand.nextInt(pirates.length);
        // Does a naive path finding algorithm that only takes into account tile types, not other blocking problems
        // Takes a start x, start y, end x, end y, and a tile type you wish to path on
        Tile[] path = getPath(pirates[i].getX(),pirates[i].getY(),pirates[target].getX(),pirates[target].getY(),0);
        // for all but the last step of the path, while I have steps, move
        for(int step=0;step+1<path.length && pirates[i].getMovesLeft()>0;step++)
        {
          pirates[i].move(path[step].getX(),path[step].getY());
        }
        // get the distance between the guys
        int distance = Math.abs(pirates[i].getX() - pirates[target].getX()) + Math.abs(pirates[i].getY()-pirates[target].getY());

        // If the distance is exactly 1 away and I don't own the guy
        if( distance ==1 && pirates[i].getOwner()!=pirates[target].getOwner())
        {
          while(pirates[i].getAttacksLeft()>0)
          {
            // attack the target
            pirates[i].attack(pirates[target]);
          }
        }
      }
    }
    return true;
  }

  //This function is called once, before your first turn
  public void init()
  {
    System.out.println("Initializing");
    rand = new Random();
  }

  //This function is called once, after your last turn
  public void end() {}


  public AI(Pointer c)
  {
    super(c);
  }
}
