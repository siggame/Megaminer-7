#!/usr/bin/env python
from dispatch import DispatchProtocol
from apps import BaseApp, protocolmethod, namedmethod, AccountsAppMixin
from itertools import repeat


import time

def fact(n):
    return reduce(lambda x,y: x*y, xrange(1,n))

class Ping(AccountsAppMixin, BaseApp):
    def __init__(self, protocol):
        BaseApp.__init__(self, protocol)
        AccountsAppMixin.__init__(self)

    @protocolmethod
    def ping(self):
        """ returns "pong" """
        return "pong"

    @protocolmethod
    def fat_ping(self):
        """ returns "pong" a whole bunch"""
        return [["pong"] for x in xrange(10000)]

    @protocolmethod
    def null(self):
        """ returns whatever is in self.value """
        return self.value

    @namedmethod("burn")
    def burn(self):
        """ sets self.value to 5! """
        self.value = fact(5)
        return None

    @protocolmethod
    def fat_burn(self):
        """ computes 1000! """
        fact(1000)
        return None

    @protocolmethod
    def whoami(self):
        if self.name:
            return ("num", self.protocol.session_num), ("name", self.name)
        else:
            return ("num", self.protocol.session_num)

class TestLatencyServer(DispatchProtocol):
    apps = Ping

    def pre_process_hook(self, line):
        print "%s sent a line." % self.session_num

    def post_process_hook(self, output):
        print "Sent a line to %s." % self.session_num
        

if __name__ == "__main__":
    TestLatencyServer.print_protocol()
    TestLatencyServer.main()
