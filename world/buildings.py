class Building:
    def __init__(self, name, enterable=False, open_hours=None):
        self.name = name
        self.enterable = enterable
        self.inside_text = "" #optional text for inside
        self.open_hours = open_hours or [] # list of (start_hour, end_hour)

    def is_open(self, hour):
        """Check if building is open given the current hour (0-23)"""
        if not self.open_hours:
            return True # no hours means always open
        for start, end in self.open_hours:
            if start <= hour < end:
                return True
        return False

# Bar
bar = Building("Bar", enterable=True, open_hours=[(14, 24)]) # 2 PM - Midnight
bar.inside_text = "The Seaside Bar, it smells of beer and smoke. Mike is behind the counter."

# Diner
diner = Building("Diner", enterable=True, open_hours=[(8, 20)]) # 8 AM - 8 PM
diner.inside_text = "The Seaside Diner, it smells like toast and fresh coffee here. Irene is behind the counter."

# Library
library = Building("Library.", enterable=True, open_hours=[(10, 16)]) # 10 AM - 4 PM
library.inside_text="The Pineport Library, that nice paper smell is in the air. Lisa Hogan is sitting behind her counter."

# Gas Station
gasstation = Building("Gas Station.", enterable=True, open_hours=[(8, 19)]) # 8 AM - 7 PM
gasstation.inside_text = "The Gas Station, Jeremy sits behind the counter reading a car magazine."

# General Store
genstore = Building("General Store", enterable=True, open_hours=[(8, 19)]) # 8 AM - 7 PM
genstore.inside_text= "The Pineport General Store, Caleb is behind the counter."

# Post Office
postoffice = Building("Post Office", enterable=True, open_hours=[(8, 16)]) # 8 AM - 4 PM
postoffice.inside_text="The Pineport Post Office, Barbara is behind the counter."

# Police Station
policestat = Building("Police Station", enterable=True, open_hours=[(8, 18)]) # 8 AM - 6 PM
policestat.inside_text="The Pineport Police Station. Forest is sitting behind his Desk."
                      
# Bank
bank = Building("Bank", enterable=True, open_hours=[(8, 16)]) # 8 AM - 4 PM
bank.inside_text="The Pineport Bank, Macey is behind the counter."

#Church
church = Building("Church", enterable=True, open_hours=[(9, 19)]) # 9 AM - 7 PM
church.inside_text="The Pineport Church, Father Dictus is here."
# NPC Houses
# Mike and Irene
ehrentraut_house = Building("The house of Mike and Irene Ehrentraut.", enterable=False)
# Jeremy and Lisa
clarksonhogan_house = Building("The house of Jeremy Clarkson and Lisa Hogan.", enterable=False)
# Caleb and Barbara
calebbarb_house = Building("The house of Caleb and Barbara Cooper.", enterable=False)
# Forest and Macey
perry_house = Building("The house of Forest and Macey Perry.", enterable=False)

dictus_house = Building("The house of Father Dictus.", enterable=False)
