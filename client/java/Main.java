import com.sun.jna.Pointer;

public class Main
{
  public static void main(String[] args)
  {
    boolean practice = false; //this must not be touched!
    if(args.length < 1)
    {
      System.out.println("Please enter a hostname");
      return;
    }

    Pointer connection = Client.INSTANCE.createConnection();

    AI ai = new AI(connection);
    if(!(Client.INSTANCE.serverConnect(connection, args[0], "19000")))
    {
      System.err.println("Unable to connect to server");
      return;
    }
    if(!(Client.INSTANCE.serverLogin(connection, ai.username(), ai.password())))
    {
      return;
    }

    if(args.length < 2)
    {
      Client.INSTANCE.createGame(connection);
    }
    else
    {
      Client.INSTANCE.joinGame(connection, Integer.parseInt(args[1]));
    }
    while(Client.INSTANCE.networkLoop(connection) != 0)
    {
      if(ai.startTurn())
      {
        Client.INSTANCE.endTurn(connection);
      }
      else
      {
        Client.INSTANCE.getStatus(connection);
      }
    }
    Client.INSTANCE.networkLoop(connection); //Grab end game state
    Client.INSTANCE.networkLoop(connection); //Grab log
    ai.end();
    return;
  }
}
