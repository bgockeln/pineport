from world.city import City, Street, Building

def load_layout(city):
    # Row 0 — Central Street
    for col in range(0, 8):
        city.place_street(col, 0, Street("Central Street"))

    # Row 1
    city.place_building(0, 1, Building("School"))
    city.place_street(1, 1, Street("Pleasant Street"))
    city.place_building(2, 1, Building("Player House"))
    city.place_building(3, 1, Building("Bar"))
    city.place_street(4, 1, Street("Main Street"))
    city.place_building(5, 1, Building("Diner"))
    city.place_street(6, 1, Street("Franklin Street"))
    city.place_building(7, 1, Building("Light House"))

    # Row 2
    city.place_building(0, 2, Building("Church"))
    city.place_street(1, 2, Street("Pleasant Street"))
    city.place_building(2, 2, Building("NPC 3's House"))
    city.place_building(3, 2, Building("Library"))
    city.place_street(4, 2, Street("Main Street"))
    city.place_building(5, 2, Building("Gas Station"))
    city.place_street(6, 2, Street("Franklin Street"))
    city.place_building(7, 2, Building("Warehouse"))

    # Row 3
    city.place_building(0, 3, Building("NPC 1's House"))
    city.place_street(1, 3, Street("Pleasant Street"))
    city.place_building(2, 3, Building("NPC 4's House"))
    city.place_building(3, 3, Building("General Store"))
    city.place_street(4, 3, Street("Main Street"))
    city.place_building(5, 3, Building("Doctor's Office"))
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
    for col in range(1, 8):
        city.place_street(col, 5, Street("Birch Street"))

def describe_location(city, x, y):
    """
    Describe the player's location with player always facing north.
    Handles vertical and horizontal streets for correct movement.
    """
    cell = city.get_cell(x, y)

    # Current cell
    if isinstance(cell.content, Street):
        print(f"You are standing on {cell.content.name}.")
        street_name = cell.content.name
    elif isinstance(cell.content, Building):
        print(f"You are in front of {cell.content.name}.")
        street_name = None
    else:
        print("You are in an unremarkable place.")
        street_name = None

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
                        print(f"{dir_name.capitalize()}, {neighbor.content.name} continues.")
                else:  # east/west
                    if ny == y:
                        print(f"{dir_name.capitalize()}, {neighbor.content.name} continues.")
            elif isinstance(neighbor.content, Building):
                print(f"{dir_name.capitalize()}, you see {neighbor.content.name}.")
            else:
                print(f"{dir_name.capitalize()}, there is nothing notable.")

