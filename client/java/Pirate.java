import com.sun.jna.Pointer;

///A basic pirate. These units are bound to land unless aboard a ship. they can pickup and drop treasure as well as build ports and fight other pirates.
class Pirate extends Unit 
{
  public Pirate(Pointer p)
  {
    super(p);
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.pirates.length; i++)
    {
      if(BaseAI.pirates[i].ID == ID)
      {
        ptr = BaseAI.pirates[i].ptr;
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
    return Client.INSTANCE.pirateMove(ptr, x, y);
  }
  ///Allows a unit to display a message to the screen.
  int talk(String message)
  {
    validify();
    return Client.INSTANCE.pirateTalk(ptr, message);
  }
  ///Attempt to attack the input target if possible
  int attack(Unit Target)
  {
    validify();
    Target.validify();
    return Client.INSTANCE.pirateAttack(ptr, Target.ptr);
  }
  ///Allows the pirate to pickup treasure on the ground.
  int pickupTreasure(int amount)
  {
    validify();
    return Client.INSTANCE.piratePickupTreasure(ptr, amount);
  }
  ///Allows the pirate to drop treasure they are carrying.
  int dropTreasure(int amount)
  {
    validify();
    return Client.INSTANCE.pirateDropTreasure(ptr, amount);
  }
  ///Pirate builds a port on a land tile with water tile adjacent. Cannot be within three spaces of another port!
  int buildPort()
  {
    validify();
    return Client.INSTANCE.pirateBuildPort(ptr);
  }
    
    //getters
    
  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.pirateGetId(ptr);
  }
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  public int getX()
  {
    validify();
    return Client.INSTANCE.pirateGetX(ptr);
  }
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  public int getY()
  {
    validify();
    return Client.INSTANCE.pirateGetY(ptr);
  }
  ///Represents the owner of the unit.
  public int getOwner()
  {
    validify();
    return Client.INSTANCE.pirateGetOwner(ptr);
  }
  ///Current ealth of the unit
  public int getHealth()
  {
    validify();
    return Client.INSTANCE.pirateGetHealth(ptr);
  }
  ///Attacking strength of the unit (Each point of strength deals 1 health of damage)
  public int getStrength()
  {
    validify();
    return Client.INSTANCE.pirateGetStrength(ptr);
  }
  ///Displays the remaining moves for this unit this turn
  public int getMovesLeft()
  {
    validify();
    return Client.INSTANCE.pirateGetMovesLeft(ptr);
  }
  ///Displays the remaining attacks for this unit this turn
  public int getAttacksLeft()
  {
    validify();
    return Client.INSTANCE.pirateGetAttacksLeft(ptr);
  }
  ///Amount of gold carried by the unit.
  public int getGold()
  {
    validify();
    return Client.INSTANCE.pirateGetGold(ptr);
  }

}
