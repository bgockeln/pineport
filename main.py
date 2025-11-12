import os
import sys
import pygame
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from world.city import City, Street
from world.buildings import Building
from renders.pygame_render import TextGUI, load_layout, describe_location
from renders.map_screen import show_map

# Get input helper function
def get_input(prompt=""):
    gui.input_text = "" #start empty
    gui.append_text(prompt) #append prompt without clearing old lines
    gui.draw
    
    while True:
        entered_text = gui.handle_events()
        gui.draw()
        if entered_text is not None:
            # Remove the prompt/input line after pressing Enter
            if gui.text_lines and gui.text_lines[-1] == prompt:
                gui.text_lines.pop()
            return entered_text

def wait():
    waiting = True
    while waiting:
        event_text = gui.handle_events()
        if event_text is not None:  # any key pressed
            waiting = False
        gui.draw()
# TextGUI
gui = TextGUI(width=900, height=700, font_size=20)



def move_player(cmd, x, y, city, player_inside):
    """Move player around the city grid. Movement blocked if inside a building."""
    if player_inside:
        gui.append_text(f"You are inside {player_inside.name}. Try 'leave {player_inside.name}' first.")
        gui.draw()
        wait()
        gui.clear_text()
        return x, y  # Cannot move while inside

    old_x, old_y = x, y
    new_x, new_y = x, y

    if cmd in ["north", "n"]:
        new_y -= 1
    elif cmd in ["south", "s"]:
        new_y += 1
    elif cmd in ["east", "e"]:
        new_x += 1
    elif cmd in ["west", "w"]:
        new_x -= 1
    else:
        return old_x, old_y

    # Bounds check
    if not (0 <= new_x < city.width and 0 <= new_y < city.height):
        gui.append_text("You can't go that way!")
        gui.draw()
        wait()
        gui.clear_text()
        return old_x, old_y

    # Deadend tiles
    blocked_tiles = {(0, 0), (7, 0), (0, 5), (7, 5)}
    if (new_x, new_y) in blocked_tiles:
        gui.append_text("The road leads to the forest here, you don't want to go there.")
        gui.draw()
        wait()
        gui.clear_text()
        return old_x, old_y

    # Only allow stepping onto streets
    target_cell = city.get_cell(new_x, new_y)
    if isinstance(target_cell.content, Street):
        gui.clear_text()
        return new_x, new_y
    else:
        gui.append_text(f"You bump into the {target_cell.content.name}. Maybe try 'enter'?")
        gui.draw()
        wait()
        gui.clear_text()
        return old_x, old_y

# Helper function for time
def format_time_12h(game_time):
    hour = int(game_time)
    minute = int((game_time % 1) * 60)
    suffix = "AM" if hour < 12 else "PM"
    display_hour = hour % 12
    if display_hour == 0:
        display_hour = 12
    return f"{display_hour:02d}:{minute:02d} {suffix}"

# Game loop
def game_loop():
    player_x, player_y = 1, 1 # Starting position
    player_inside = None # None means outside

    city = City(width = 8, height = 6)
    load_layout(city)

    gui.clear_text()
    if not player_inside:
        describe_location(city, player_x, player_y, gui)

    game_time = 8.0 # start at noon (24 hour clock)

    while True:
        cmd = gui.handle_events()
        gui.draw()

        if cmd is None:
            continue  # wait for input
        
        cmd = cmd.lower()

        # Increment time
        game_time = (game_time + 0.1) % 24

        # Update status bar
        gui.set_status(time=game_time)

        # Update NPCs
        for npc in city.npcs:
            npc.update(game_time)

        ### Commands ###

        # 1. Movement
        if cmd in ("north", "n", "south", "s", "east", "e", "west", "w"):
            player_x, player_y = move_player(cmd, player_x, player_y, city, player_inside)
            if not player_inside:
                describe_location(city, player_x, player_y, gui)
        
        # 2. Actions
        # Look
        elif cmd in ("look", "l"):
            if not player_inside:
                describe_location(city, player_x, player_y, gui)
            elif player_inside:
                gui.append_text("Poop")

        # Enter
        elif cmd.startswith("enter"):
            if player_inside:
                gui.append_text(f"You are already inside {player_inside.name}")
                gui.draw()
                continue

            target_name = cmd.replace("enter", "", 1).strip()
            building = city.get_nearby_building(player_x, player_y, target_name)
            if not building:
                gui.append_text("There is nothing to enter here.")
                gui.draw()
                continue

            current_hour = game_time % 24

            if not building.enterable:
                gui.append_text(f"{building.name} is locked.")
                gui.draw()
                continue

            if hasattr(building, "open_hours") and building.open_hours:
                if not building.is_open(current_hour):
                    gui.append_text(f"{building.name} is closed right now.")
                    gui.draw()
                    continue

            # Player enters building
            player_inside = building
            gui.clear_text()
            gui.append_text(f"You enter {building.name}.")
            if building.inside_text:
                gui.append_text(building.inside_text)
            gui.draw()


        # Leave command
        elif cmd.startswith("leave"):
            if not player_inside:
                gui.append_text("You are not inside any building.")
                gui.draw()
                continue

            leaving_name = cmd.replace("leave", "", 1).strip()

            # check if typed name matches the building partially
            if leaving_name not in player_inside.name.lower(): 
                gui.append_text(f"You are inside {player_inside.name}, not {leaving_name}.")
                gui.draw()
                continue

            gui.append_text(f"You leave {player_inside.name}.")
            gui.draw()
            player_inside = None
            describe_location(city, player_x, player_y, gui)

        # Talk
        elif cmd.startswith("talk"):
            gui.append_text("There is nobody to talk to yet")
            gui.draw()

        # Help
        elif cmd in ("help", "h"):
            gui.append_text("Available commands are: ")
            gui.append_text("Movement: north, south, east, west or n, s, e, w")
            gui.append_text("Actions: look or l, talk, exit or quit")
            gui.draw()

        # Toggle map
        elif cmd == "m" or cmd == "map":
            show_map(city, player_x, player_y, gui.screen)
            gui.clear_text()
            if not player_inside:
                describe_location(city, player_x, player_y, gui)
            # Add code to handle map inside buildings

        # Quit
        elif cmd in ("quit", "exit"):
            gui.append_text("Exiting game")
            gui.draw()
            wait()
            break

        else: 
            gui.append_text("Unknown command, type Help for a list of commands")

# Main menu
def main_menu():
    gui.clear_text()
    gui.append_text("Welcome to Pineport")
    gui.append_text("A small fishing Town in New England.")
    gui.append_text("This is less of a game and more of an experiment.")
    gui.append_text("The goal is to see if I can simulate a very simple town")
    gui.append_text("and its residents in python")
    gui.append_text("Press any key")
    gui.draw()
    wait()

    gui.clear_text()
    gui.append_text("1. New Game")
    gui.append_text("2. Change language")
    gui.append_text("3. Exit Game")

    gui.draw()
    choice = get_input("Choice: ")

    if choice == "1":
        gui.clear_text()
        game_loop()
    elif choice == "3":
        pygame.quit()
        sys.exit(0)
    else:
        gui.clear_text()
        gui.append_text("Invalid input")
        gui.draw()
        wait()
        main_menu()  # restart men

def main():
    main_menu()

if __name__ == "__main__":
    main()