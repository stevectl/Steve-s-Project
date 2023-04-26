from datetime import datetime, timedelta, date
from Amenity import SharedAmenity, InRoomAmenity
import Guest, Booking, Bed

class Hotel:
    """
    this class initializes name, Guest class, amenity, an empty booking dict, and takes in txt filename and sets up room availability
    functions are created for to search/add roomavailabilty, amenity, guests and bookings
    """
    def __init__(self, name, roomFilename):
        self._name = name
        self._guests = self.setupGuests()
        self._amenities = self.setupAmenities()
        self._roomAvailability = self.setupRoomAvailability(roomFilename)
        self._bookings = {}

    def setupGuests(self):

        guests = {}

        infile = open("Guests.txt", "r")
        for line in infile:
            pp, name, country = line.split(",")
            guests[pp.strip()] = Guest.Guest(pp.strip(), name.strip(), country.strip())
        infile.close()

        infile = open("Blacklist.txt", "r")
        for line in infile:
            pp, dateReported, reason = line.split(",")
            g = guests.get(pp.strip())
            if g is not None:
                g.blacklist(datetime.strptime(dateReported.strip(), "%d-%b-%Y").date(), reason.strip())
        infile.close()

        return guests

    def setupAmenities(self):

        amenities = []

        infile = open("SharedAmenity.txt", "r")
        for line in infile:
            itemCode, desc, price = line.split(",")
            amenities.append(SharedAmenity(itemCode, desc, float(price)))
        infile.close()

        infile = open("InRoomAmenity.txt", "r")
        for line in infile:
            itemCode, desc, price, floorArea = line.split(",")
            amenities.append(InRoomAmenity(itemCode, desc, float(price), float(floorArea)))

        infile.close()

        return amenities

    def setupRoomAvailability(self, filename):

        roomAvailability = {}

        infile = open(filename, "r")
        for line in infile:
            dateString, standardCount, deluxeCount = line.split(",")
            thisDate = datetime.strptime(dateString, "%d-%b-%Y").date()
            roomAvailability[thisDate] = [int(standardCount), int(deluxeCount)]
        infile.close()

        return roomAvailability

    def saveRoomAvailability(self, filename):

        outfile = open(filename, "w")

        for k, v in self._roomAvailability.items():
            print("{},{},{}".format(k.strftime("%d-%b-%Y"), v[0], v[1]), file=outfile)
        outfile.close()

    
    def searchGuests(self, passportNo):
        """searches if passport is in the keys of guest[]"""
        if passportNo in self._guests.keys():
            return self._guests[passportNo]
        else:
            return None


    def checkRoomAvailability(self, startDate, endDate):
        """
        searches if there is room available on specified date. takes in class Date parameter and checks if checkout is after checkin
        if checkout date < checkin date or date is not in room availability, return false
        iterates through the dictionary to ensure room is available throughout duration of dates
        """
        flag = 0
        if (startDate >= endDate) or (startDate not in self._roomAvailability.keys()):
            return False
        
        else:
            while startDate <= endDate:
                if startDate in self._roomAvailability.keys():
                    flag = 1
                    startDate += timedelta(days=1) 
                else:
                    flag = 0
                    break
        
        if flag == 0:
            return False
        elif flag == 1:
            return True


    def listAmenity(self):
        """iterate through amenity list and list it out"""
        text = ""
        for i in self._amenities:
            text += str(i)+"\n"
        return text

    def getAmenity(self, itemCode):
        """iterate through amenity list, if itemCode matches amenity item, return item"""
        for i in self._amenities:
            if i.getItemCode == itemCode:
                return i
            else:
                pass
        return None

    def searchBooking(self, bookingID):
        """searches if bookingID is in dictionary keys"""
        if bookingID in self._bookings.keys():
            return self._bookings[bookingID]
        else:
            return None
        
    def searchBookingByPassport(self, passport):
        """iterate through booking dictionary, if passport matches object.getPassport, return object"""
        for bookings in self._bookings.keys():

            if passport == self._bookings[bookings].getPassport:
                return self._bookings[bookings]
            else:
                pass
        return []
        
    def submitBooking(self, newBooking:Booking):
        """
        stores checkinDate into var, checks if var is in keys and status is pending.
        iterates through from checkin to checkout date and ensure room count is available, deduct 1 if room is available.
        store remaining rooms into .txt file, set booking as confirmed
        """
        bookingDate = newBooking.getCheckInDate

        if bookingDate not in self._roomAvailability.keys():
            print("Room is not available on specified dates!")

        else:
            #checks if bookingStatus is pending and if checkinDate is in roomAvaillabity {}
            if (newBooking.getStatus == "Pending"):
                
                #runs check from checkin to checkout
                while bookingDate <= newBooking.getCheckOutDate:
                    
                    #var to set standard and deluxe room count
                    stdRoomCount = self._roomAvailability[bookingDate][0]
                    deluxeRoomCount = self._roomAvailability[bookingDate][1]
                
                    if (newBooking.getRoomType == "Standard") and (bookingDate in self._roomAvailability.keys()):
                        if stdRoomCount > 0:
                            stdRoomCount -= 1
                        else:
                            raise Bed.BookingException("Standard Room is unavailable on {}".format(bookingDate.strftime("%d-%b-%Y")))

                    elif (newBooking.getRoomType == "Deluxe") and (bookingDate in self._roomAvailability.keys()):
                        if deluxeRoomCount > 0:
                            deluxeRoomCount -= 1
                        else:
                            raise Bed.BookingException("Deluxe Room is unavailable on {}".format(bookingDate.strftime("%d-%b-%Y")))

                    self._roomAvailability[bookingDate][0] = stdRoomCount
                    self._roomAvailability[bookingDate][1] = deluxeRoomCount

                    bookingDate += timedelta(days=1) 
 
            else:
                raise Bed.BookingException("Specified booking does not exist!")
            
            self.saveRoomAvailability("Rooms_April2023.txt")
            self._bookings[newBooking.getBookingID] = newBooking
            newBooking.setStatus("Confirmed")
            print("Booking is submitted.")

    def cancelBooking(self, bookingID):
        """
        if bookingID in booking dict, check if booking is confirmed.
        iterate through checkin to checkout date, +1 roomcount to selected rooms.
        stores roomcount in .txt file and sets booking to cancelled
        """
        if bookingID in self._bookings.keys():
            
            if self._bookings[bookingID].getStatus != "Confirmed":
                raise Bed.BookingException("This booking is not confirmed yet, cant be cancelled!!")
            
            else:
                checkInDateFormatted = datetime.strptime(str(self._bookings[bookingID].getCheckInDate), "%Y-%m-%d").date()
                checkOutDateFormatted = datetime.strptime(str(self._bookings[bookingID].getCheckOutDate), "%Y-%m-%d").date()

                while checkInDateFormatted <= checkOutDateFormatted:
                
                    #var to set standard and deluxe room count
                    stdRoomCount = self._roomAvailability[checkInDateFormatted][0]
                    deluxeRoomCount = self._roomAvailability[checkInDateFormatted][1]

                    if (self._bookings[bookingID].getRoomType == "Standard") and (checkInDateFormatted in self._roomAvailability.keys()):
                        stdRoomCount += 1
                    elif (self._bookings[bookingID].getRoomType == "Deluxe") and (checkInDateFormatted in self._roomAvailability.keys()):
                        deluxeRoomCount += 1

                    self._roomAvailability[checkInDateFormatted][0] = stdRoomCount
                    self._roomAvailability[checkInDateFormatted][1] = deluxeRoomCount

                    checkInDateFormatted += timedelta(days=1) 

                self._bookings[bookingID].setStatus("Cancelled")
                self._bookings.pop(bookingID)
                self.saveRoomAvailability("Rooms_April2023.txt")
                print("Booking is cancelled....")
        else:
            raise Bed.BookingException("Booking ID does not exist!")


    def checkIn(self, bookingID, allocatedRoomNo):
        """check into room if booking ID is in booking dict"""
        
        if self._bookings[bookingID].getCheckInDate == date.today():
            
            if bookingID in self._bookings.keys():
                self._bookings[bookingID].checkIn(allocatedRoomNo)
            else:
                raise Bed.BookingException("Booking does not exist!")
        
        else:
            raise Bed.BookingException("Cannot check in today!!")