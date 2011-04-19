#!/usr/bin/env python
try:
    from twisted.internet import epollreactor
    epollreactor.install()
except:
    pass

from twisted.internet import protocol, reactor, defer
from twisted.protocols.basic import LineReceiver
import random
import time
from numpy import array

class TestClient(protocol.Protocol):
    clients = []
    latencies = []
    i = 0
    def connectionMade(self):
        self.n = TestClient.i
        TestClient.i += 1
        self.t = time.time()
        self.queue = 0

    def send_message(self):
        self.t = time.time()
        self.transport.write('("whoami") ("login" "test" "test" ) ("whoami") ("burn") ("null")\r\n')

    def queue_message(self):
        if not(self.queue):
            self.send_message()
        else:
            self.queue += 1
            
    def dataReceived(self, line):
        t = time.time()
        print t-self.t
        print line
        TestClient.latencies.append(t-self.t)
        if self.queue:
            self.queue -= 1
            self.send_message()
        
def protocol_created(p):
    TestClient.clients.append(p)

def pick_and_send():
    if TestClient.clients: random.choice(TestClient.clients).send_message()
    reactor.callLater(0.02, pick_and_send)

def start_sessions():
    for i in range(1000):
        cc = protocol.ClientCreator(reactor, TestClient)
        d = cc.connectTCP("127.0.0.1", 3001)
        d.addCallback(protocol_created)
    reactor.callLater(0, pick_and_send)

reactor.callLater(0, start_sessions)
reactor.run()
