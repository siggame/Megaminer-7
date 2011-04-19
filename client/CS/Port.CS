using System;
using System.Runtime.InteropServices;


///A basic port. The port can create new pirates and ships and is used when pirates need to deposit money.
public class Port: Mappable 
{
  
  public Port()
  {
  }
  
  public Port(IntPtr p)
  {
    ptr = p;
    ID = Client.portGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public override bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.ports.Length; i++)
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
  public int createPirate()
  {
    validify();
    return Client.portCreatePirate(ptr);
  }
  ///Creates a Ship at the calling Port
  public int createShip()
  {
    validify();
    return Client.portCreateShip(ptr);
  }
    
    //getters
    
  ///Unique Identifier
  public new int getId()
  {
    validify();
    return Client.portGetId(ptr);
  }
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  public new int getX()
  {
    validify();
    return Client.portGetX(ptr);
  }
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  public new int getY()
  {
    validify();
    return Client.portGetY(ptr);
  }
  ///The ownder of the port
  public int getOwner()
  {
    validify();
    return Client.portGetOwner(ptr);
  }

}
