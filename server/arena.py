import aspects
import sys

from game_app.match import Match

from twisted.internet import reactor

games = []

def install():
  def wrapMatch(*args, **kwargs):
    yield aspects.proceed
    f = open('created', 'w')
    f.write('Game created')
    f.close()
    
    
  def wrapStart(*args, **kwargs):
    yield aspects.proceed
    f = open('started', 'w')
    f.write('Game started')
    f.close()

  def wrapDeclareWinner(self, winner, reason):
    f = open('winner', 'w')
    if winner is self.players[0]:
      f.write("Player 0 wins")
    else:
      f.write("Player 1 wins")
    f.close()
    yield aspects.proceed
    reactor.stop()

  aspects.with_wrap(wrapMatch, Match.__init__)
  aspects.with_wrap(wrapStart, Match.start)
  aspects.with_wrap(wrapDeclareWinner, Match.declareWinner)
