import com.sun.jna.Pointer;

///A basic ship. They can only travel by sea and attack other ships. Whenever the ship moves, any pirates on his tile go with it
class Ship extends Unit 
{
  public Ship(Pointer p)
  {
    super(p);
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.ships.length; i++)
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
  int move(int x, int y)
  {
    validify();
    return Client.INSTANCE.shipMove(ptr, x, y);
  }
  ///Allows a unit to display a message to the screen.
  int talk(String message)
  {
    validify();
    return Client.INSTANCE.shipTalk(ptr, message);
  }
  ///Attempt to attack the input target if possible
  int attack(Unit Target)
  {
    validify();
    Target.validify();
    return Client.INSTANCE.shipAttack(ptr, Target.ptr);
  }
    
    //getters
    
  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.shipGetId(ptr);
  }
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  public int getX()
  {
    validify();
    return Client.INSTANCE.shipGetX(ptr);
  }
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  public int getY()
  {
    validify();
    return Client.INSTANCE.shipGetY(ptr);
  }
  ///Represents the owner of the unit.
  public int getOwner()
  {
    validify();
    return Client.INSTANCE.shipGetOwner(ptr);
  }
  ///Current ealth of the unit
  public int getHealth()
  {
    validify();
    return Client.INSTANCE.shipGetHealth(ptr);
  }
  ///Attacking strength of the unit (Each point of strength deals 1 health of damage)
  public int getStrength()
  {
    validify();
    return Client.INSTANCE.shipGetStrength(ptr);
  }
  ///Displays the remaining moves for this unit this turn
  public int getMovesLeft()
  {
    validify();
    return Client.INSTANCE.shipGetMovesLeft(ptr);
  }
  ///Displays the remaining attacks for this unit this turn
  public int getAttacksLeft()
  {
    validify();
    return Client.INSTANCE.shipGetAttacksLeft(ptr);
  }
  ///Amount of gold carried by the unit.
  public int getGold()
  {
    validify();
    return Client.INSTANCE.shipGetGold(ptr);
  }

}
