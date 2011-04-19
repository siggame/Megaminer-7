# -*- coding: iso-8859-1 -*-
from abc import ABCMeta
from collections import defaultdict
from functools import wraps
import string
import traceback
import WebServerAuthenticator

import config.config

def namedmethod(name):
  def inner(f):
      f._name = name
      f.is_protocol = True
      return f
  return inner

def dashify(str):
  if not str:
    return str
  result = str[0].lower()
  for i in str[1:]:
    if i in string.uppercase:
      result += '-'
    result += i.lower()
  return result

def protocolmethod(f):
  name = dashify(f.__name__)
  return namedmethod(name)(f)

class Protocol(type):
  def __new__(cls, name, bases, attrs):
      _mapper = {}
      for d in ([base.__dict__ for base in bases] + [attrs]):
          for attrname, attrvalue in d.iteritems():
              if getattr(attrvalue, 'is_protocol', 0):
                  _mapper[attrvalue._name] = attrvalue
          attrs["_mapper"] = _mapper
      return super(Protocol, cls).__new__(cls, name, bases, attrs)

class BaseApp(object):
  __metaclass__ = Protocol
  wrapper = {}
  
  def __init__(self, protocol):
    self.protocol = protocol

  def run(self, coms):
    try:
      command = self.__class__._mapper[coms[0]]
      return command(self, *coms[1:])
    except KeyError as e:
      traceback.print_exc()
      return "invalid-command",  coms[0]
    except Exception as e:
      traceback.print_exc()
      return "unknown-error", ("command", coms[0]), ("arguments", coms[1:])

  def disconnect(self, reason):
    pass

class AccountsAppMixin(object):
  def __init__(self):
    self.logged_in = False
    self.name = None
  
  @protocolmethod
  def login(self, name, password):
    #THIS IS THE OLD CODE FOR VERIFYING LOGIN STUFFz
    #validNames = config.config.readConfig("config/login.cfg")
    #if (name in validNames and validNames[name]["password"] == password):
    #  self.logged_in = True
    #  self.name = name
    #  return ["login-accepted"]
    #return ["login-denied"]
    
    
    #THIS IS THE NEW CODE THAT VERIFIES LOGIN WITH AWESOME WEB SERVER!!!
    
    webAuth = WebServerAuthenticator.WebServerAuthenticator("megaminerai.com")
    
    try:
      val = webAuth.auth_team(name, password)
      if (val):
        self.logged_in = True
        self.name = str(val)
        return ["login-accepted"]
      else:
        return ["login-denied"]
    except WebServerAuthenticator.WebServerException:
      return ["login-denied"]
    

  @protocolmethod
  def logout(self):
    self.logged_in = False

  
