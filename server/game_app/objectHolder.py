import objects

class ObjectHolder(dict):
  def __init__(self, *args, **kwargs):
    dict.__init__(self, *args, **kwargs)
    self.pirates = []
    self.ships = []
    self.tiles = []
    self.ports = []
    self.players = []
    self.treasures = []

  def __setitem__(self, key, value):
    if key in self:
      self.__delitem__(key)
    dict.__setitem__(self, key, value)
    if isinstance(value, objects.Pirate):
      self.pirates.append(value)
    if isinstance(value, objects.Ship):
      self.ships.append(value)
    if isinstance(value, objects.Tile):
      self.tiles.append(value)
    if isinstance(value, objects.Port):
      self.ports.append(value)
    if isinstance(value, objects.Player):
      self.players.append(value)
    if isinstance(value, objects.Treasure):
      self.treasures.append(value)

  def __delitem__(self, key):
    value = self[key]
    dict.__delitem__(self, key)
    for i in self.pirates, self.ships, self.tiles, self.ports, self.players, self.treasures:
      if value in i:
        i.remove(value)

