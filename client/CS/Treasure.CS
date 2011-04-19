using System;
using System.Runtime.InteropServices;


///This is the source of your wealth. When dropped on the ground it will build interest baed on its distance to pirates, if dropped on a port it is added to your ooverall wealth
public class Treasure: Mappable 
{
  
  public Treasure()
  {
  }
  
  public Treasure(IntPtr p)
  {
    ptr = p;
    ID = Client.treasureGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public override bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.treasures.Length; i++)
    {
      if(BaseAI.treasures[i].ID == ID)
      {
        ptr = BaseAI.treasures[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }
    
    //commands
    
    
    //getters
    
  ///Unique Identifier
  public new int getId()
  {
    validify();
    return Client.treasureGetId(ptr);
  }
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  public new int getX()
  {
    validify();
    return Client.treasureGetX(ptr);
  }
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  public new int getY()
  {
    validify();
    return Client.treasureGetY(ptr);
  }
  ///The amount of gold currently with this treasure
  public int getGold()
  {
    validify();
    return Client.treasureGetGold(ptr);
  }

}
