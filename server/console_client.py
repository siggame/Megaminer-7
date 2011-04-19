#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
try:
    from twisted.internet import epollreactor
    epollreactor.install()
except:
    pass

from twisted.internet import protocol, reactor, defer
from twisted.protocols.basic import Int32StringReceiver
import random
import time
import threading

class ConsoleClient(Int32StringReceiver):
  clients = []
  latencies = []
  i = 0
  def connectionMade(self):
    self.n = ConsoleClient.i
    ConsoleClient.i += 1
    self.t = time.time()
    self.queue = 0

  def send_message(self):
    self.t = time.time()
    self.sendString('("whoami") ("login" "test" "test" ) ("whoami") ("burn") ("null")\r\n')

  def queue_message(self):
    if not(self.queue):
      self.send_message()
    else:
      self.queue += 1
      
  def stringReceived(self, line):
    t = time.time()
    print t-self.t
    print line
    ConsoleClient.latencies.append(t-self.t)
    if self.queue:
      self.queue -= 1
      self.send_message()

  def startConsole(self):
    exitCmd = ['exit', 'quit', 'done']
    print "Enter the messages you want to send to the server"
    print "Example: (whoami)"
    print "To exit, type exit, quit, or done"
    message = ""
    while (message not in ['exit', 'quit', 'done']):
      message = raw_input()
      self.sendString(message)
        
def protocol_created(p):
  ConsoleClient.clients.append(p)
  consoleThread = threading.Thread(target=ConsoleClient.startConsole, args=(p,))
  consoleThread.start()

def pick_and_send():
  if ConsoleClient.clients: random.choice(ConsoleClient.clients).send_message()
  reactor.callLater(0.02, pick_and_send)

def start_sessions():
  cc = protocol.ClientCreator(reactor, ConsoleClient)
  d = cc.connectTCP("127.0.0.1", 19000)
  d.addCallback(protocol_created)
  #reactor.callLater(0, cc.startConsole())

reactor.callLater(0, start_sessions)
reactor.run()
