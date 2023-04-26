from abc import abstractmethod


class Amenity:
    """
    Main class for all amenities, common attributes are here
    this class sets up Amenity by initialising itemCode, desc, and price
    there are 2 subclass of Amenity, which has another floorArea variable to initialise
    """
    def __init__(self, itemCode:str , description:str , price:float):
        self._itemCode = itemCode
        self._description = description
        self._price = price

    @property
    def getItemCode(self):
        return self._itemCode
    
    @property
    def getPrice(self):
        return self._price
    
    @abstractmethod
    def getFloorArea(self):
        pass

    def __str__(self):
        return "{}, {}, {:.2f}".format(self._itemCode, self._description, self._price)
        


class InRoomAmenity(Amenity):
    """Sub-class of amenity, has attributes of in-room amenites"""
    def __init__(self, itemCode, description, price, floorArea:float):
        super().__init__(itemCode, description, price)
        self._floorArea = floorArea

    @property
    def getFloorArea(self):
        return self._floorArea

    def __str__(self):
        return "{}, {}, ${:.2f}, {}m".format(self._itemCode, self._description, self._price, self.getFloorArea)


class SharedAmenity(Amenity):
    """Sub-class of amenity, has attributes of shared amenities"""

    def __init__(self, itemCode, description, price):
        super().__init__(itemCode, description, price)

    @property
    def getFloorArea(self):
        return 0
    
    def __str__(self):
        return "{}, {}, ${:.2f}, {}m".format(self._itemCode, self._description, self._price, self.getFloorArea)
    
def main():

    ia1 = InRoomAmenity("DESK-W","Writing desk (80cm x 55cm)",3.99,0.44)
    ia2 = InRoomAmenity("CHAIR","Foldable Chair (42cm x 38cm)",2.59,0.16)

    sa1 = SharedAmenity("BREAKFAST","Breakfast buffet at Sun café (Level 1-01 6am to 10am)",8.99)
    sa2 = SharedAmenity("HI-TEA","Hi-Tea buffet at Sun café (Level 1-01 2pm to 4pm)",11.99)

    totalFloorArea = ia1.getFloorArea + ia2.getFloorArea
    
    print("Total floor area: ", totalFloorArea)

    totalPrice = ia1.getPrice + ia2.getPrice + sa1.getPrice + sa2.getPrice

    print("Total price: ${:.2f}".format(totalPrice))

main()