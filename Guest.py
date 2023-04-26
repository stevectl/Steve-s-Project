class Guest:
    """
    this class sets up Guest class and initializes with passport, name, and country
    there is 2 function set up to blacklist and show blacklist history of guests
    """
    
    def __init__(self, passport:str , name:str , country:str):
        self._passport = passport
        self._name = name
        self._country = country
        self._blacklistedReason = []

    @property
    def getName(self):
        return self._name
 
    @property
    def getPassport(self):
        return self._passport   

    
    def isBlacklisted(self):
        """if blacklistedReason is empty return false, else true"""
        if len(self._blacklistedReason) == 0:
            return False
        else:
            return True
              
    
    def blacklist(self, dateReported, reason):
        """takes in parameter from calling function and stores in nested list"""
        self.dateReported = dateReported
        self.reason = reason
        self._blacklistedReason.append([dateReported, reason])
        
    
    def __str__(self):

        text = ("\nPassport Number: {}\nName: {}\nCountry: {}\n".format(self._passport, self._name, self._country))

        if self.isBlacklisted():
            text += "<< Blacklisted on date, reason >>"
            for i in range(len(self._blacklistedReason)):
                text += "\n> {}\t{}".format(self._blacklistedReason[i][0], self._blacklistedReason[i][1])
            
        else:
            text += "Not blacklisted"
        return text