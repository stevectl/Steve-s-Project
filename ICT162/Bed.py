class Bed:
  """
  this class sets up Bed by initialising type, price, and desc
  there is a class variable which consists of bed type and floorArea
  2 custom Exceptions are also in here
  """

  _TYPE_SIZE = {"Single":1.73, "Super":2.03}

  def __init__(self, type:str , price:float , description:str):
      self._type = type
      self._price = price
      self._description = description
      
  @property
  def getPrice(self):
      return self._price
  
  @property
  def getFloorArea(self):
      #if type of bed in typesize, return floorArea value
      if self._type in self._TYPE_SIZE:
          return self._TYPE_SIZE[self._type]
      
  
  def __str__(self):
      return "{}, ${:.2f}".format(self._description, self._price)


class BookingException(Exception):
  pass


class MinFloorAreaException(Exception):
  pass

