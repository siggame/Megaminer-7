import com.sun.jna.Pointer;

///A basic port. The port can create new pirates and ships and is used when pirates need to deposit money.
class Port extends Mappable 
{
  public Port(Pointer p)
  {
    super(p);
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.ports.length; i++)
    {
      if(BaseAI.ports[i].ID == ID)
      {
        ptr = BaseAI.ports[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }
    
    //commands
    
  ///Creates a Pirate at the calling Port
  int createPirate()
  {
    validify();
    return Client.INSTANCE.portCreatePirate(ptr);
  }
  ///Creates a Ship at the calling Port
  int createShip()
  {
    validify();
    return Client.INSTANCE.portCreateShip(ptr);
  }
    
    //getters
    
  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.portGetId(ptr);
  }
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  public int getX()
  {
    validify();
    return Client.INSTANCE.portGetX(ptr);
  }
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  public int getY()
  {
    validify();
    return Client.INSTANCE.portGetY(ptr);
  }
  ///The ownder of the port
  public int getOwner()
  {
    validify();
    return Client.INSTANCE.portGetOwner(ptr);
  }

}
