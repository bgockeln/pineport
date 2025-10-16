import time as pytime
from .buildings import Building, bar
from .npc import NPC

class Cell:
    def __init__(self, x, y, content=None):
        self.x = x
        self.y = y
        self.content = content # Street or Building or None
        self.npcs_here = []

class Street:
    def __init__(self, name):
        self.name = name

class City:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.npcs = []

    def place_building(self, x, y, building):
        self.grid[y][x].content = building
    
    def place_street(self, x, y, street):
        self.grid[y][x].content = street

    def add_npc(self, npc, x, y):
        cell = self.get_cell(x, y)
        npc.location = cell
        cell.npcs_here.append(npc)
        self.npcs.append(npc)

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def update(self, current_time):
        for npc in self.npcs:
            npc.update(current_time, self)

    def run(self):
        # game clock in HH:MM
        hour, minute = 8, 0
        while True:
            current_time = f"{hour:02d}:{minute:02d}"
            self.update(current_time)
            self.display()  # a method to print grid / NPCs

            # advance game time
            minute += 1  # 1 in-game minute per loop
            if minute >= 60:
                minute = 0
                hour += 1
                if hour >= 24:
                    hour = 0

            # real-time wait, e.g., 0.1 sec per game minute
            pytime.sleep(0.1)
        
    def display(self):
        # prints the grid / NPCs
        print("\033[H\033[J")  # clear screen (ANSI escape)
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell.npcs_here:
                    row += "N "
                elif isinstance(cell.content, Street):
                    row += "S "
                elif isinstance(cell.content, Building):
                    row += "B "
                else:
                    row += ". "
            print(row)

    @staticmethod
    def next_time(current_time):
        hour, minute = map(int, current_time.split(":"))
        hour += 1
        if hour >= 24:
            hour = 0
        return f"{hour:02d}:{minute:02d}"
    
    def get_nearby_building(self, x, y, name=None):
        """Return the building at (x, y) or in an adjacent cell, optionally filtered by name"""
        directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Boundary check
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
            
            cell = self.get_cell(x + dx, y + dy)
            if isinstance(cell.content, Building):
                if not name or name.lower() in cell.content.name.lower():
                    return cell.content
        return None