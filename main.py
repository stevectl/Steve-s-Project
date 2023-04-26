from datetime import datetime, timedelta
import Booking, Bed, Hotel, Room


def option1(Hotel):
    """
    Submit Booking
    take in passport and checks if guest is registered. Asks for preferred room and bed type.
    allows user to select list of amenities to add, breaks the loop if input is Enter
    takes in check in/out date in DD-MMM-YYYY format
    """
    guestPassport = input("\nEnter Passport Number to start: ").upper()

    if Hotel.searchGuests(guestPassport) == None:
        print("You are not a registered guest!")

    else:
        guestProfile = Hotel.searchGuests(guestPassport)
        print("Guest located. Please verify\n", guestProfile, "\n")

        while True:
            roomType = input("Select preferred room type (S)tandard or (D)eluxe: ").upper()
            if roomType == "":
                print("That option is invalid!")
            elif roomType in "SD":
                break
            else:
                print("That option is invalid!")
        
        while True:
            bedType = input("Select preferred bed type (S)ingle or s(U)per: ").upper()
            if bedType == "":
                print("That option is invalid!")
            elif bedType in "SU":
                break
            else:
                print("That option is invalid!")

        r1 = None
        b1 = None

        if bedType == "S":
            b1 = Bed.Bed("Single", 10.99, "Single bed with one pillow and one blanket")
        elif bedType == "U":
            b1 = Bed.Bed("Super", 12.99, "Super single bed with one pillow and one blanket")
            
        if roomType == "S":
            r1 = Room.Room("Standard", 16.99, b1) 
        elif roomType == "D":
            r1 = Room.Room("Deluxe", 19.99, b1)

        print("\nList of Amenities\n=================\n", Hotel.listAmenity())

        amenityChoice = None

        while True:

            amenityChoice = input("Enter item code to add or <enter> to stop: ").upper()

            if (Hotel.getAmenity(amenityChoice)) != None:
                try:
                    r1.addAmenity(Hotel.getAmenity(amenityChoice))
                    print(amenityChoice + " added...")
                except Bed.BookingException as e:
                    print(e)
            
            elif amenityChoice == "":
                break

            elif (Hotel.getAmenity(amenityChoice)) == None:
                print("Specified item does not exist!")


        checkInString = input("Enter check in date: ")
        checkOutString = input("Enter check out date: ")

        try:
            #convert from class string to class Date
            checkInDate = datetime.strptime(checkInString, "%d-%b-%Y").date()
            checkOutDate = datetime.strptime(checkOutString, "%d-%b-%Y").date()
        except:
            print("Please enter in DD-MMM-YYYY format!")
            return

        if Hotel.checkRoomAvailability(checkInDate, checkOutDate) == False:
            print("Check In/Out duration is not available!!")
            return

        try:
            book1 = Booking.Booking(guestProfile, r1, checkInDate, checkOutDate)
            print("\nPlease verify Guest and Room details....\n\n", book1)
        except Bed.BookingException as e:
            print(e)
            return

        while True:
            userSubmitBooking = input("\nProceed to submit booking? (Y/N): ").upper()
            if userSubmitBooking == "Y":
                try:
                    Hotel.submitBooking(book1)
                    break

                except Bed.BookingException as e:
                    print(e)
                    break

            elif userSubmitBooking == "N":
                print("Your booking as been cancelled.")
                break
            else:
                print("That option is invalid!")

def option2(Hotel):
    """
    Cancel Booking
    takes in bookingID in integer format and cancel booking
    """
    while True:
        idToCancel = input("Enter booking ID to cancel: ")

        try:
            idToCancel = int(idToCancel)
            Hotel.cancelBooking(idToCancel)
        except Bed.BookingException as e:
            print(e)
        except:
            print("Please enter a valid booking ID")
        break

def option3(Hotel):
    """
    Search Booking
    2 methods of searching:
    search by bookingID takes in ID as integer and inputs as parameter for Hotel.searchBooking
    search by passport take in passport as string and inputs as parameter for Hotel.searchBookingByPassport
    """
    while True:
        searchMethod = input("Search by Booking ID or Passport? (B/P): ").upper()
        if searchMethod == "B":
            bookingID = input("Enter Booking ID to search: ")

            try:
                bookingID = int(bookingID)
            except:
                print("Please enter a valid booking ID!")
                break
        
            if Hotel.searchBooking(bookingID) == None:
                print("This booking does not exist!")
            else:
                print(Hotel.searchBooking(bookingID))
            break

        elif searchMethod == "P":
            passport = input("Enter passport number to search: ").upper()
            
            if Hotel.searchBookingByPassport(passport) == []:
                print("This booking does not exist!")
            else:
                print(Hotel.searchBookingByPassport(passport))
            break
        else:
            print("Please enter a valid option")

def option4(Hotel):
    """
    Check-In
    takes in bookingID as integer. if bookingID is in booking dictionary, return booking object.
    Enter the allocated room  number and press Enter to check-in. only integer input are valid as room number
    """
    bookingID = input("Enter Booking ID to start Check-In: ")
    
    try:
        bookingID = int(bookingID)
    except:
        print("Please enter a valid booking ID!")

    if Hotel.searchBooking(bookingID) == None:
        print("This booking does not exist!")

    else:
        print("Please verify Guest and Room details....")
        print(Hotel.searchBooking(bookingID))
        
        roomNumber = input("Enter allocated room number or <enter> to cancel Check-In: ")
        if roomNumber == "":
            print("You have cancelled your Check-In.")
        try:
            roomNumber = int(roomNumber)
        except:
            print("Please enter a valid booking ID!")
        try:
            Hotel.checkIn(bookingID, roomNumber)
        except Bed.BookingException as e:
            print(e)
            

def main():
    import os

    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in %r: %s" % (cwd, files))
    """
    a seperate main() function to reduce code clutter.
    prints 4 options that runs 4 diff functions
    1. Submit Booking
    2. Cancel Booking
    3. Search Booking(s)
    4. Check-In
    """

    #variables
    roomAvailability = "Rooms_April2023.txt"

    #creating hotel object
    h1 = Hotel.Hotel("Hotel California", roomAvailability)

    userChoice = input("@@@@ SAMI HOTEL @@@@\n====================\n1. Submit Booking\n2. Cancel Booking\n3. Search Booking(s)\n4. Check-In\n0. Exit\nEnter option: ")
    while userChoice != "0":
        if userChoice == "1":
            option1(h1)
        elif userChoice == "2":
            option2(h1)
        elif userChoice == "3":
            option3(h1)
        elif userChoice == "4":
            option4(h1)
        elif userChoice == "0":
            break
        else:
            print("Please enter a valid option!")

        userChoice = input("@@@@ SAMI HOTEL @@@@\n====================\n1. Submit Booking\n2. Cancel Booking\n3. Search Booking(s)\n4. Check-In\n0. Exit\nEnter option: ")


main()