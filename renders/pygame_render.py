import pygame
import sys
from world.buildings import Building, bar, diner, library, gasstation, ehrentraut_house, clarksonhogan_house
from world.city import City, Street
from world.npc import mike, irene


class TextGUI:
    def __init__(self, width=800, height=600, font_size=20, line_spacing=5):
        pygame.init()
        self.width = width
        self.height = height
        self.font_size = font_size
        self.line_spacing = line_spacing

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pineport")

        self.font = pygame.font.SysFont("monospace", font_size)
        self.clock = pygame.time.Clock()

        # Colors
        self.bg_color = (0, 0, 0)
        self.status_color = (200, 200, 200)
        self.text_color = (255, 255, 255)
        self.input_color = (0, 255, 0)

        # Text buffers
        self.status = ""
        self.text_lines = []
        self.input_text = ""

        # Layout sizes
        self.status_height = font_size + 10
        self.input_height = font_size + 10
        self.text_area_height = self.height - self.status_height - self.input_height

        # Max lines that fit in the text area
        self.max_lines = self.text_area_height // (font_size + line_spacing)

    def set_status(self, text="", time=None):
        """ 
        Update status bar text. Optionally pass current time (float)
        """
        if time is not None:
            hours = int(time) % 24
            minutes = int((time - int(time)) * 60)
            suffix = "AM" if hours < 12 else "PM"
            display_hour = hours % 12
            if display_hour == 0:
                display_hour = 12
            time_str = f"{display_hour:02d}:{minutes:02d} {suffix}"
            self.status = f"{text}  Time: {time_str}"
        else:
            self.status = text

    def append_text(self, text):
        """Append text with word wrapping so it fits inside the window"""
        for raw_line in text.split("\n"):
            words = raw_line.split(" ")
            line = ""
            for word in words:
                test_line = line + word + " "
                # check width in pixels
                if self.font.size(test_line)[0] > self.width - 40: # leave padding
                    self.text_lines.append(line.strip())
                    line = word + " "
                else:
                    line = test_line
            if line:
                self.text_lines.append(line.strip())

        #for line in text.split("\n"):
        #    self.text_lines.append(line)
        if len(self.text_lines) > self.max_lines:
            self.text_lines = self.text_lines[-self.max_lines:]

    def clear_text(self):
        self.text_lines = []

    def handle_events(self):
        entered_text = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            # Only access event.key if this is a KEYDOWN event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entered_text = self.input_text
                    self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

        return entered_text
    
    def draw(self):
        self.screen.fill(self.bg_color)

        # Draw status bar
        pygame.draw.rect(self.screen, (50, 50, 50), (0, 0, self.width, self.status_height))
        status_surf = self.font.render(self.status, True, self.status_color)
        self.screen.blit(status_surf, (5, 5))

        # Draw text area
        y = self.status_height
        for line in self.text_lines[-self.max_lines:]:
            surf = self.font.render(line, True, self.text_color)
            self.screen.blit(surf, (5, y))
            y += self.font_size + self.line_spacing

        # Draw input line
        pygame.draw.rect(self.screen, (30, 30, 30),
                         (0, self.height - self.input_height, self.width, self.input_height))
        input_surf = self.font.render("Command: " + self.input_text, True, self.input_color)
        self.screen.blit(input_surf, (5, self.height - self.input_height + 5))

        pygame.display.flip()
        self.clock.tick(30)

def load_layout(city):
    # Row 0 — Central Street
    for col in range(0, 8):
        city.place_street(col, 0, Street("Central Street"))

    # Row 1
    city.place_building(0, 1, Building("School"))
    city.place_street(1, 1, Street("Pleasant Street"))
    city.place_building(2, 1, Building("Player House"))
    city.place_building(3, 1, bar)
    city.place_street(4, 1, Street("Main Street"))
    city.place_building(5, 1, diner)
    city.place_street(6, 1, Street("Franklin Street"))
    city.place_building(7, 1, Building("Light House"))

    # Row 2
    city.place_building(0, 2, Building("Church"))
    city.place_street(1, 2, Street("Pleasant Street"))
    city.place_building(2, 2, ehrentraut_house)
    city.place_building(3, 2, library)
    city.place_street(4, 2, Street("Main Street"))
    city.place_building(5, 2, gasstation)
    city.place_street(6, 2, Street("Franklin Street"))
    city.place_building(7, 2, Building("Warehouse"))

    # Row 3
    city.place_building(0, 3, clarksonhogan_house)
    city.place_street(1, 3, Street("Pleasant Street"))
    city.place_building(2, 3, Building("NPC 4's House"))
    city.place_building(3, 3, Building("General Store"))
    city.place_street(4, 3, Street("Main Street"))
    city.place_building(5, 3, Building("Bank"))
    city.place_street(6, 3, Street("Franklin Street"))
    city.place_building(7, 3, Building("Fishing Docks"))

    # Row 4
    city.place_building(0, 4, Building("NPC 2's House"))
    city.place_street(1, 4, Street("Pleasant Street"))
    city.place_building(2, 4, Building("NPC 5's House"))
    city.place_building(3, 4, Building("Police Station"))
    city.place_street(4, 4, Street("Main Street"))
    city.place_building(5, 4, Building("Post Office"))
    city.place_street(6, 4, Street("Franklin Street"))
    city.place_building(7, 4, Building("Pier"))

    # Row 5 — Birch Street
    for col in range(0, 8):
        city.place_street(col, 5, Street("Birch Street"))

def describe_location(city, x, y, gui):
    """
    Describe the player's location with player always facing north.
    Handles vertical and horizontal streets for correct movement.
    """
    gui.clear_text()
    cell = city.get_cell(x, y)

    # Current cell
    if isinstance(cell.content, Street):
        gui.append_text(f"You are standing on {cell.content.name}.")
    elif isinstance(cell.content, Building):
        gui.append_text(f"You are in front of {cell.content.name}.")
    else:
       gui.append_text("You are in an unremarkable place.")


    # Directions relative to player-facing-north
    neighbors = {
        "in front of you (north)": (x, y-1),
        "behind you (south)": (x, y+1),
        "to your right (east)": (x+1, y),
        "to your left (west)": (x-1, y)
    }

    for dir_name, (nx, ny) in neighbors.items():
        neighbor = city.get_cell(nx, ny)
        if neighbor:
            if isinstance(neighbor.content, Street):
                # Continue logic for orientation
                if "north" in dir_name or "south" in dir_name:  # vertical movement
                    if nx == x:
                        gui.append_text(f"{dir_name.capitalize()}, {neighbor.content.name} continues.")
                else:  # east/west
                    if ny == y:
                        gui.append_text(f"{dir_name.capitalize()}, {neighbor.content.name} continues.")
            elif isinstance(neighbor.content, Building):
                gui.append_text(f"{dir_name.capitalize()}, you see {neighbor.content.name}.")
            else:
                gui.append_text(f"{dir_name.capitalize()}, there is nothing notable.")