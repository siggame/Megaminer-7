import com.sun.jna.Pointer;

///An object that exists on the grid
abstract class Mappable
{
  Pointer ptr;
  int ID;
  int iteration;
  public Mappable(Pointer p)
  {
    ptr = p;
    ID = Client.INSTANCE.mappableGetId(ptr);
    iteration = BaseAI.iteration;
  }
  abstract boolean validify();
    
    //commands
    
    
    //getters
    
  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.mappableGetId(ptr);
  }
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  public int getX()
  {
    validify();
    return Client.INSTANCE.mappableGetX(ptr);
  }
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  public int getY()
  {
    validify();
    return Client.INSTANCE.mappableGetY(ptr);
  }

}
