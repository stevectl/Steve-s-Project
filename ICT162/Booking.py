import Bed, Guest, Room

class Booking:
    """
    this class sets up Booking by initialising Guest,Room, checkinDate and checkoutDate
    there is a class variable which is bookingID
    upon initializing, this class will run checks to see if guest is blacklisted and also checks on the checkin/out date
    there is a checkIn func for Guests to check in and also a totalPrice calculator to return fullPrice of room * number of nights
    """

    _NEXT_ID = 1

    def __init__(self, guest:Guest, room:Room, checkInDate, checkOutDate):
        
        self._guest = guest
        self._checkInDate = checkInDate
        self._checkOutDate = checkOutDate

        if self._guest.isBlacklisted():
            raise Bed.BookingException("Guest is blacklisted")
        
        elif self._checkInDate >= self._checkOutDate:
            raise Bed.BookingException("Please ensure check in/out dates are valid")

        self._room = room
        self._bookingID = Booking._NEXT_ID
        self._allocatedRoomNo = None
        self._status = "Pending"
        Booking._NEXT_ID += 1

    @property
    def getBookingID(self):
        return self._bookingID

    @property
    def getCheckInDate(self):
        return self._checkInDate

    @property
    def getCheckOutDate(self):
        return self._checkOutDate

    @property
    def getStatus(self):
        return self._status

    @property
    def getPassport(self):
        return self._guest.getPassport

    @property
    def getRoomType(self):
        return self._room.getType

    @property
    def getTotalPrice(self):
        numOfNights = (self.getCheckOutDate - self.getCheckInDate).days
        return numOfNights * self._room.fullPrice

    def setStatus(self, newStatus:str):
        self._status = newStatus

    
    def checkIn(self, allocatedRoomNo):
        """checkin status checks if confirmed first, before checking blacklist. then allows checkin """
        
        if  self.getStatus != "Confirmed":
            raise Bed.BookingException("Your booking is not confirmed!")

        elif (self._guest.isBlacklisted() == True):
            raise Bed.BookingException("Guest is blacklisted!")
    
        else:
            print("Check-In success!")
            self._status = "Checked-In"
            self._allocatedRoomNo = allocatedRoomNo

    def __str__(self):
        text = "Booking ID: {} \nPassport Number: {} \nName: {} \nCheck-In/Out dates: {} / {} \nBooking Status: {} \n\n{} \nTotal Price: ${:.2f} x {} night = ${:.2f}".format(self.getBookingID, self._guest.getPassport, self._guest.getName, self.getCheckInDate.strftime("%d-%b-%Y"), self.getCheckOutDate.strftime("%d-%b-%Y"), self.getStatus, self._room, self._room.fullPrice, ((self.getCheckOutDate - self.getCheckInDate).days), self.getTotalPrice)
        return text