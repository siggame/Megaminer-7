import aspects

from game_app.match import Match
from game_app.objects import Player
from twisted.internet import reactor

games = []

def install():
  def wrapNextTurn(self):
    if self not in games:
      games.append(self)
    if self.turn == self.players[0]:
      p = [i for i in self.objects.players]
      p[1].time += self.timeInc
    elif self.turn == self.players[1]:
      p = [i for i in self.objects.players]
      p[0].time += self.timeInc
    retval = yield aspects.proceed

  aspects.with_wrap(wrapNextTurn, Match.nextTurn)

  def tick():
    import main
    for i in games:
      p = [j for j in i.objects.values() if isinstance(j,Player)]
      if i.turn == i.players[0]:
        p[0].time -= 1
        if p[0].time < 0:
          print "2 Wins!"
          i.declareWinner(i.players[1], 'Player 1 Lagged Out, Player 2 Wins')
      elif i.turn == i.players[1]:
        p[1].time -= 1
        if p[1].time < 0:
          print "1 Wins!"
          i.declareWinner(i.players[0], 'Player 2 Lagged Out, Player 1 Wins')
      else:
        games.remove(i)

    reactor.callLater(1, tick)

  reactor.callWhenRunning(reactor.callLater, 1, tick)
        
