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
bar = Building("The Seaside Bar", enterable=True, open_hours=[(14, 24)]) # 2 PM - Midnight
bar.inside_text = "The bar smells of beer and smoke. Mike is behind the counter."

# Diner
diner = Building("The Seaside Diner", enterable=True, open_hours=[(8, 20)]) # 8 AM - 8 PM
diner.inside_text = "Smells like toast and fresh coffee here. Irense is behind the counter."

# Library
library = Building("The Library.", enterable=True, open_hours=[(10, 16)]) # 10 AM - 4 PM
library.inside_text="That nice paper smell is in the air. Lisa Hogan is sitting behind her counter"

# Gas Station
gasstation = Building("The Gas Station.", enterable=True, open_hours=[(8, 19)]) # 8 am - 7 pm
gasstation.inside_text = "Jeremy sits behind the counter with car magazine"

#NPC Houses
ehrentraut_house = Building("Mike and Irene Ehrentraut live here", enterable=False)
clarksonhogan_house = Building("Jeremy Clarkson and Lisa Hogan live here", enterable=False)