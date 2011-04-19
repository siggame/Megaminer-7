using System;
using System.Runtime.InteropServices;


///A basic ship. They can only travel by sea and attack other ships. Whenever the ship moves, any pirates on his tile go with it
public class Ship: Unit 
{
  
  public Ship()
  {
  }
  
  public Ship(IntPtr p)
  {
    ptr = p;
    ID = Client.shipGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public override bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.ships.Length; i++)
    {
      if(BaseAI.ships[i].ID == ID)
      {
        ptr = BaseAI.ships[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }
    
    //commands
    
  ///Move the unit to the designated X and Y coordinates if possible
  public new int move(int x, int y)
  {
    validify();
    return Client.shipMove(ptr, x, y);
  }
  ///Allows a unit to display a message to the screen.
  public new int talk(string message)
  {
    validify();
    return Client.shipTalk(ptr, message);
  }
  ///Attempt to attack the input target if possible
  public new int attack(Unit Target)
  {
    validify();
    Target.validify();
    return Client.shipAttack(ptr, Target.ptr);
  }
    
    //getters
    
  ///Unique Identifier
  public new int getId()
  {
    validify();
    return Client.shipGetId(ptr);
  }
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  public new int getX()
  {
    validify();
    return Client.shipGetX(ptr);
  }
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  public new int getY()
  {
    validify();
    return Client.shipGetY(ptr);
  }
  ///Represents the owner of the unit.
  public new int getOwner()
  {
    validify();
    return Client.shipGetOwner(ptr);
  }
  ///Current ealth of the unit
  public new int getHealth()
  {
    validify();
    return Client.shipGetHealth(ptr);
  }
  ///Attacking strength of the unit (Each point of strength deals 1 health of damage)
  public new int getStrength()
  {
    validify();
    return Client.shipGetStrength(ptr);
  }
  ///Displays the remaining moves for this unit this turn
  public new int getMovesLeft()
  {
    validify();
    return Client.shipGetMovesLeft(ptr);
  }
  ///Displays the remaining attacks for this unit this turn
  public new int getAttacksLeft()
  {
    validify();
    return Client.shipGetAttacksLeft(ptr);
  }
  ///Amount of gold carried by the unit.
  public new int getGold()
  {
    validify();
    return Client.shipGetGold(ptr);
  }

}
