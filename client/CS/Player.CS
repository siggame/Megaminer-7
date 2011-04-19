using System;
using System.Runtime.InteropServices;


///
public class Player
{
  public IntPtr ptr;
  protected int ID;
  protected int iteration;
  
  public Player()
  {
  }
  
  public Player(IntPtr p)
  {
    ptr = p;
    ID = Client.playerGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.players.Length; i++)
    {
      if(BaseAI.players[i].ID == ID)
      {
        ptr = BaseAI.players[i].ptr;
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
    return Client.playerGetId(ptr);
  }
  ///Player's Name
  public string getPlayerName()
  {
    validify();
    return Client.playerGetPlayerName(ptr);
  }
  ///Player's Gold
  public int getGold()
  {
    validify();
    return Client.playerGetGold(ptr);
  }
  ///Time remaining
  public int getTime()
  {
    validify();
    return Client.playerGetTime(ptr);
  }

}
