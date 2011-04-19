public class ExistentialError : System.ApplicationException
{
  public ExistentialError() : base("Object does not exist anymore.")
  {}
}
