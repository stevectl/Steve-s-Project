from tkinter import *
from datetime import datetime
import Hotel, main


class MainGUI:

    def __init__(self):
        self._hotelName = "Hotel California"
        self.roomAvailability = "Rooms_April2023.txt"
        self._hotel = Hotel.Hotel(self._hotelName, self.roomAvailability)

        self._window = Tk()
        self._window.title("Main GUI - done by Steve Chia")
        self._window.geometry('1280x1000')

        self.passportFrame = Frame(master=self._window, width=200, height=30)
        self.passportFrame.pack(fill=X)

        self.dateReportedFrame = Frame(master=self._window, width=200, height=30)
        self.dateReportedFrame.pack(fill=X)

        self.reasonsFrame = Frame(master=self._window, width=200, height=30)
        self.reasonsFrame.pack(fill=X)

        self.searchButtonFrame = Frame(master=self._window, width=200, height=40)
        self.searchButtonFrame.pack(fill=X)

        self.textboxFrame = Frame(master=self._window)
        self.textboxFrame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.passportLabel = Label(master=self.passportFrame, text="Enter your options")
        self.passportLabel.place(x=0, y=0)
        self.passportEntry = Entry(master=self.passportFrame)
        self.passportEntry.place(x=100, y=0)

        self.dateReportedLabel = Label(master=self.dateReportedFrame, text="Date reported:")
        self.dateReportedLabel.place(x=0, y=0)
        self.dateReportedEntry = Entry(master=self.dateReportedFrame, width=30, state="disabled")
        self.dateReportedEntry.place(x=100, y=0)
        self.dateReportedLabel = Label(master=self.dateReportedFrame, text="DD-MMM-YYYY")
        self.dateReportedLabel.place(x=300, y=0)

        self.reasonsLabel = Label(master=self.reasonsFrame, text="Reason(s):")
        self.reasonsLabel.place(x=0, y=0)
        self.reasonEntry = Entry(master=self.reasonsFrame, width=30, state="disabled")
        self.reasonEntry.place(x=100, y=0)

        self.searchButton = Button(master=self.searchButtonFrame, text="Search", width=10, background="white", command=self.searchButton)
        self.searchButton.place(x=40, y=0)

        self.blacklistButton = Button(master=self.searchButtonFrame, text="Blacklist", width=10, background="white", state=DISABLED, command=self.blacklistButton)
        self.blacklistButton.place(x=140, y=0)

        self.resetButton = Button(master=self.searchButtonFrame, text="Reset", width=10, command=self.resetButton)
        self.resetButton.place(x=240, y=0)

        self.textbox = Text(master=self.textboxFrame, height=10, width=50, state="disabled")
        self.textbox.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self._window.mainloop()

#--------------------------------------FUNCTIONS--------------------------------------
    def searchButton(self):
        self.textbox['state'] = NORMAL
        self.textbox.delete(1.0, END)
        self.textbox['state'] = DISABLED

        passport = self.passportEntry.get().upper()

        if self._hotel.searchGuests(passport) is None:
            self.textbox['state'] = NORMAL
            self.textbox.insert(END, "Unable to locate guest with this passport number.")
            self.textbox['state'] = DISABLED

        else:
            self.searchButton['state'] = DISABLED
            self.passportEntry['state'] = DISABLED
            self.dateReportedEntry['state'] = NORMAL        
            self.dateReportedEntry.focus_set()
            self.reasonEntry['state'] = NORMAL
            self.blacklistButton['state'] = NORMAL

            self.textbox['state'] = NORMAL
            self.textbox.insert(INSERT, self._hotel.searchGuests(passport))
            self.textbox.insert(INSERT, "\n\nEnter date and reason to blacklist.....\n")
            self.textbox['state'] = DISABLED

        #changes Reset button state
        if len(self.textbox.get(1.0, END)) > 1:
            self.resetButton['state'] = NORMAL
        else:
            self.resetButton['state'] = DISABLED

    def resetButton(self):
        self.searchButton['state'] = NORMAL

        self.passportEntry['state'] = NORMAL
        self.passportEntry.delete(0, END)

        self.dateReportedEntry['state'] = NORMAL
        self.dateReportedEntry.delete(0, END)
        self.dateReportedEntry['state'] = DISABLED

        self.reasonEntry['state'] = NORMAL
        self.reasonEntry.delete(0, END)
        self.reasonEntry['state'] = DISABLED

        self.textbox['state'] = NORMAL
        self.textbox.delete(1.0, END)
        self.textbox['state'] = DISABLED

        self.blacklistButton['state'] = DISABLED
        self.resetButton['state'] = DISABLED

        self.passportEntry.focus_set()

    def blacklistWriteOut(self, passport, date, reason):
        outfile = open("Blacklist.txt", "a")
        print("{}, {}, {}".format(passport, date, reason), file=outfile)
        outfile.close()
        
    def blacklistButton(self):
        passport =  self.passportEntry.get().upper()
        guestProfile = self._hotel.searchGuests(passport)
        dateReported =  self.dateReportedEntry.get()
        reason =  self.reasonEntry.get()

        try:
            formattedDateReported = datetime.strptime(dateReported, "%d-%b-%Y").date()
        except:
            self.textbox['state'] = NORMAL
            self.textbox.insert(END, "\n\nPlease enter datetime in DD-MMM-YYYY format...\n(e.g. 1-Jan-2023)")
            self.textbox['state'] = DISABLED

        if len(reason) < 1:
            self.textbox['state'] = NORMAL
            self.textbox.insert(END, "\n\nReason for blacklist must not be empty")
            self.textbox['state'] = DISABLED
        else:
            guestProfile.blacklist(formattedDateReported, reason)

            self.textbox['state'] = NORMAL
            self.textbox.insert(END, guestProfile)
            self.textbox['state'] = DISABLED
            self.blacklistWriteOut(passport, dateReported, reason)
#--------------------------------------FUNCTIONS--------------------------------------

MainGUI()