#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import functools
import string

def dashify(str):
  if not str:
    return str
  result = str[0].lower()
  for i in str[1:]:
    if i in string.uppercase:
      result += '-'
    result += i.lower()
  return result

def errorBuffer(func):
  """
  A decorator.
  Allows all of the game_app's functions to just return either
  True or an error string
  Makes the function instead return (protocol-name, True) on success or
  (protocol-name, False, error-message) on failure
  """
  @functools.wraps(func)
  def wrappedFunc(self, *args):
    errBuff = func(self, *args)
    name = dashify(func.__name__)
    if errBuff == True:
      return False
    else:
      return (name + '-denied', errBuff)
  return wrappedFunc

def requireLogin(func):
  """
  A decorator.
  Prevents this method from running successfully unless the connection
  is logged in.
  """
  @functools.wraps(func)
  def wrappedFunc(self, *args):
    if not self.logged_in:
      return "You are not logged in"
    else:
      return func(self, *args)
  return wrappedFunc

def requireGame(func):
  """
  A decorator.
  Prevents this method from running successfully unless the connection
  is logged in and associated with a game
  """
  @functools.wraps(func)
  @requireLogin
  def wrappedFunc(self, *args):
    if self.game is None:
      return "You are not in a game"
    else:
      return func(self, *args)
  return wrappedFunc

def requireTurn(func):
  """
  A decorator.
  Prevents this method from running successfully unless the connection
  is logged in, associated with a game, and is the current player
  """

  @functools.wraps(func)
  @requireGame
  def wrappedFunc(self, *args):
    if self.game.turn is not self:
      return "It is not your turn"
    else:
      return func(self, *args)
  return wrappedFunc


def requireTypes(*types):
  """
  A decorator maker.
  Converts all of the arguements to the specified types, or returns an
  error if the conversions fail.
  types[i] is the type for args[i] to the original function (or None).
  """
  def decorator(func):
    @functools.wraps(func)
    def wrappedFunc(*args):
      newargs = []
      if len(args) != len(types):
        return "Expected %d arguements (Received %d)"%(len(types),         len(args))
      for i in xrange(len(args)):
        if types[i] is None:
          newargs.append(args[i])
        elif types[i] in [int, str, float]:
          try:
            newargs.append(types[i](args[i]))
          except ValueError:
            return "Invalid type for argument %d"%(i,)
      return func(*newargs)
    return wrappedFunc
  return decorator

