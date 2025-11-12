class NPC:
    def __init__(self, name, home, work=None, schedule=None):
        self.name = name
        self.home = home
        self.work = work
        self.schedule = schedule
        self.location = home # nps starting position 
        self.current_activity = "at home"

    def update(self, current_time):
        """Update NPC location and activity base on current time (in hours)"""
        for (start, end), place in self.schedule.items():
            if start <= current_time < end:
                if self.location != place:
                    self.location = place
                    self.current_activity = "working" if place == self.work else "at home"
                return
        # if no schedule matches, default home
        self.location = self.home
        self.current_activity = "sleeping"
        
mike = NPC(
    name="Mike Ehrentraut",
    home=(2, 2),
    work=(3, 1),
    schedule={
        (14, 24): (3, 1), # works from 2 pm till 0 am at the bar
        (0, 2): (2, 2),     # home
        (2, 14): (2, 2) #home
    }
)

irene = NPC(
    name="Irene Ehrentraut",
    home=(2, 2),
    work=(5, 1),
    schedule={
        (8, 20): (5, 1), # works from 8 am till 8 pm at the diner
        (20, 24): (2, 2), # home
        (0, 8): (2, 2) # home
    }
)

jeremy = NPC(
    name="Jeremy Clarkson",
    home=(0, 3),
    work=(5, 2),
    schedule={
        (8, 19): (5, 2), # works from 8 am till 7 pm at the gastation
        (19, 24): (3, 2), # home
        (0, 8): (3, 2) #home
    }
)

lisa = NPC(
    name="Lisa Hogan",
    home=(0, 3),
    work=(3, 2),
    schedule={
        (10, 16): (3, 2), # works from 10 till to 4 pm
        (16, 24): (0, 3), # home
        (0, 10): (3, 3) # home
    }
)

caleb = NPC(
    name="Caleb Cooper",
    home=(0, 4),
    work=(3, 3),
    schedule={
        (8, 19): (5, 3), # works from 8 am till 7 pm
        (19, 24): (0, 4), # home
        (0, 8): (0, 4) # home
    }
)

barbara = NPC(
    name="Barbara Cooper",
    home=(0, 4),
    work=(5, 4),
    schedule={
        (8, 16): (5, 4), # works from 8 am till 4 pm
        (16, 24): (0, 4), # home
        (0, 8): (0, 4) # home
    }
) 

forest = NPC(
    name="Forest Perry",
    home=(2, 3),
    work=(3, 4),
    schedule={
        (8, 18): (3, 4), # works from 8 am to 6 pm
        (18, 24): (2, 3), # home
        (0, 8): (2, 3) # home
    }
)

macey = NPC(
    name="Macey Perry",
    home=(2, 3),
    work=(5, 3),
    schedule={
        (8, 16): (5, 3), # works from 8 am till 4 pm
        (16, 24): (2, 3), # home
        (0, 8): (2, 3) # home
    }
)

dictus = NPC(
    name="Father Dictus",
    home=(2, 4),
    work=(0, 2),
    schedule={
        (9, 19): (0, 2), #works from 9 am till 7 pm
        (19, 24): (2, 4), # home
        (0, 9): (2, 4) # home
    }
)