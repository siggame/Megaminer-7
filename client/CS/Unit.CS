using System;
using System.Runtime.InteropServices;


///Generic Unit
public abstract class Unit: Mappable 
{
  
  public Unit()
  {
  }
  
  public Unit(IntPtr p)
  {
    ptr = p;
    ID = Client.unitGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public abstract override bool validify();
    
    //commands
    
  ///Move the unit to the designated X and Y coordinates if possible
  public int move(int x, int y)
  {
    validify();
    return Client.unitMove(ptr, x, y);
  }
  ///Allows a unit to display a message to the screen.
  public int talk(string message)
  {
    validify();
    return Client.unitTalk(ptr, message);
  }
  ///Attempt to attack the input target if possible
  public int attack(Unit Target)
  {
    validify();
    Target.validify();
    return Client.unitAttack(ptr, Target.ptr);
  }
    
    //getters
    
  ///Unique Identifier
  public new int getId()
  {
    validify();
    return Client.unitGetId(ptr);
  }
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  public new int getX()
  {
    validify();
    return Client.unitGetX(ptr);
  }
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  public new int getY()
  {
    validify();
    return Client.unitGetY(ptr);
  }
  ///Represents the owner of the unit.
  public int getOwner()
  {
    validify();
    return Client.unitGetOwner(ptr);
  }
  ///Current ealth of the unit
  public int getHealth()
  {
    validify();
    return Client.unitGetHealth(ptr);
  }
  ///Attacking strength of the unit (Each point of strength deals 1 health of damage)
  public int getStrength()
  {
    validify();
    return Client.unitGetStrength(ptr);
  }
  ///Displays the remaining moves for this unit this turn
  public int getMovesLeft()
  {
    validify();
    return Client.unitGetMovesLeft(ptr);
  }
  ///Displays the remaining attacks for this unit this turn
  public int getAttacksLeft()
  {
    validify();
    return Client.unitGetAttacksLeft(ptr);
  }
  ///Amount of gold carried by the unit.
  public int getGold()
  {
    validify();
    return Client.unitGetGold(ptr);
  }

}
