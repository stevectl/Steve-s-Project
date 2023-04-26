import Bed, Amenity

class Room:
  """
  this class sets up Room by initialising roomtype, roomprice, and Bed object. sets empty list to amenities attribute
  fullPrice() returns the room price * no. of night
  add/remove amenities will insert/pop objects from list
  """
  _MIN_EXIT_SPACE =  1.84
  _TYPE_SIZE = {"Standard": 4.2, "Deluxe": 4.83}

  def __init__(self, type:str , roomPrice:float , bed:Bed):
    self._type = type
    self._roomPrice = roomPrice
    self._bed = bed
    self._amenities = []

  @property
  def getType(self):
    return self._type

  @property
  def getRoomPrice(self):
    return self._roomPrice

  @property
  def fullPrice(self):
    """this function calculates the price of room+bed+amenities and returns total price"""
    roomFullPrice = 0
    roomFullPrice += self._roomPrice + self._bed.getPrice
    for i in self._amenities:
      roomFullPrice += i.getPrice
    return roomFullPrice
  
 
  def addAmenity(self, newItem:Amenity):
    """ Used to add amenity, checks for no duplicate and items+room is less than safe space area"""

    #checks for duplicates
    if self._amenities.count(newItem) != 0:
      raise Bed.BookingException("You can only have 1 type of amenity per room")
      
    #checks if new item added exceeds min exit space
    elif self._TYPE_SIZE[self._type] - newItem.getFloorArea < self._MIN_EXIT_SPACE:
      raise Bed.MinFloorAreaException("There is not enough space in your room to fit more amenities.")

    #appends amenity to amenityList and adds into floorArea
    else:
      self._amenities.append(newItem)
      self._TYPE_SIZE[self._type] -= newItem.getFloorArea



  def removeAmenity(self, itemCode:str):
    """ 
    Used to remove amenity, iterate through amenity list, if itemCode matches, pop item and remove from floorArea
    iterate through the list, if itemCode is found, pop object.
    """
    flag = 0
    for i in self._amenities:
      
      if i.getItemCode == itemCode:
        self._amenities.remove(i)
        self._TYPE_SIZE[self._type] += i.getFloorArea
        flag = 1
        break
        
      else:
        pass
    
    if flag == 0:
      raise Bed.BookingException("No such amenity!!!")



  def __str__(self):
    
    text = "{} room, ${:.2f} \n{}, ${:.2f}".format(self._type, self._roomPrice, self._bed._description, self._bed.getPrice)
    for i in self._amenities:
      text += "\n{}, ${:.2f}".format(i._description, i.getPrice)
    text += "\nFull Price: ${:.2f}\n".format(self.fullPrice)

    return text


def main():

  single = Bed.Bed("Single", 10.99, "Single bed with one pillow and one blanket")
  superSingle = Bed.Bed("Super", 12.99, "Super single bed with one pillow and one blanket")
  
  deluxeRoom = Room("Deluxe", 19.99, superSingle)
  standardRoom = Room("Standard", 16.99, single) 

  miniFridge = Amenity.InRoomAmenity("FRIDGE","Mini Fridge (50L)",4.59,0.25)
  chair = Amenity.InRoomAmenity("CHAIR","Foldable Chair (42cm x 38cm)",2.59,0.16)
  desk = Amenity.InRoomAmenity("DESK-W","Writing desk (80cm x 55cm)",3.99,0.44)
  iron = Amenity.InRoomAmenity("IRON-B","Iron and ironing board (128cm x 30cm)",2.99,0.4)
  
  gymPass = Amenity.SharedAmenity("GYM-PEP","Per entry pass to gym (Level 4-01)",1.00)
  wifi = Amenity.SharedAmenity("WI-FI","One-day Wi-Fi access",1.00)
  

  try:
    deluxeRoom.addAmenity(miniFridge)
    deluxeRoom.addAmenity(chair)
    deluxeRoom.addAmenity(desk)
    deluxeRoom.addAmenity(iron)
  except Bed.BookingException as e:
    print(e)
  print("\n", deluxeRoom)


  try:
    standardRoom.addAmenity(gymPass)
    standardRoom.addAmenity(miniFridge)
    standardRoom.addAmenity(wifi)
    standardRoom.addAmenity(gymPass)
  except Bed.BookingException as e:
    print(e)
  print("\n", standardRoom)


  try:
    deluxeRoom.removeAmenity("FRIDGE")
    deluxeRoom.removeAmenity("GYM-PEP")
  except Bed.BookingException as e:
    print(e)
  print("\n", deluxeRoom)


  try:
    standardRoom.removeAmenity("FRIDGE")
    standardRoom.removeAmenity("GYM-PEP")
  except Bed.BookingException as e:
    print(e)
  print("\n", standardRoom)

  
main()