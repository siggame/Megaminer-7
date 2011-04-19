"""
config.py
Creator: Josh Bohde
Description: Module to parse config
"""

from ConfigParser import SafeConfigParser

def formatAttr(n):
    """
    function formatAttr
    casts an arbitrary string to either an int or float, if it can
    """
    try:
        return int(n)
    except:
        pass
    try:
        return float(n)
    except:
        pass
    if (n[0] == '['):
        return eval(n)
    return n

def readConfig(cfgfile):
        """
        function readConfig
        reads the config file, and parses it.
        """
        contents = dict()
        cparse = SafeConfigParser()
        cparse.optionxform = str
        cparse.read(cfgfile)
        for key in cparse.sections():
            contents[key] = dict([(item[0], formatAttr(item[1])) for item in cparse.items(key)])
        return contents

def getUserInfo(user, cfgfile):
    """getUserInfo
       returns a dictionary containing the attribute value pairs
       as specified in the given config file, or returns None if no such
       information is present."""
    userInfo = dict()
    cparse = SafeConfigParser()
    cparse.optionxform = str
    cparse.read(cfgfile)
    key = user
    if cparse.has_section(key):
        userInfo = dict([(item[0], str(item[1])) for item in cparse.items(key)])
        if 'screenName' not in userInfo:
            userInfo['screenName'] = user
    else:
        userInfo = None
    return userInfo

if __name__ == "__main__":
   print getUserInfo("Shell AI", 'config/login.cfg')
