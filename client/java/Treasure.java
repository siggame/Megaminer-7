import com.sun.jna.Pointer;

///This is the source of your wealth. When dropped on the ground it will build interest baed on its distance to pirates, if dropped on a port it is added to your ooverall wealth
class Treasure extends Mappable 
{
  public Treasure(Pointer p)
  {
    super(p);
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.treasures.length; i++)
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
  public int getId()
  {
    validify();
    return Client.INSTANCE.treasureGetId(ptr);
  }
  ///The X position of this object.  X is horizontal, with 0,0 as the top left corner
  public int getX()
  {
    validify();
    return Client.INSTANCE.treasureGetX(ptr);
  }
  ///The Y position of this object.  Y is vertical, with 0,0 as the top left corner
  public int getY()
  {
    validify();
    return Client.INSTANCE.treasureGetY(ptr);
  }
  ///The amount of gold currently with this treasure
  public int getGold()
  {
    validify();
    return Client.INSTANCE.treasureGetGold(ptr);
  }

}
