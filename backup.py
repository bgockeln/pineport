import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from world.city import City
from renders.cli_render import load_layout, describe_location





# clear screen helper function
def clear_screen():
    os.system("cls" if os.name=="nt" else "clear")

# wait for input helper function
def wait():
    input("Press any key")

# Game loop
def start_game():
    city = City(width = 8, height = 6)
    load_layout(city)

    player_x, player_y = 1, 1 # Starting position

    while True:
        describe_location(city, player_x, player_y)
        cmd = input("Where do you want to go= (north/south/east/west) ")

        if cmd.lower() in ["north", "n"] and player_y > 0:
            player_y -= 1
            clear_screen()
        elif cmd.lower() in ["south", "s"] and player_y < city.height - 1:
            player_y += 1
            clear_screen()
        elif cmd.lower() in ["east", "e"] and player_x < city.width - 1:
            player_x += 1
            clear_screen()
        elif cmd.lower() in ["west", "w"] and player_x > 0:
            player_x -= 1
        elif cmd.lower() in ("exit", "quit"):
            print("Exiting game...")
            break
        else:
            print("You can't go that way!")

# Main menu
def main_menu():
    clear_screen()
    print("Welcome to Pineport")
    print("A small fishing Town in New England.")
    print("This is less of a game and more of an experiment.")
    print("The goal is to see if I can simulate a very simple town")
    print("and its residents in python")
    wait()
    clear_screen()
    print("1. New Game")
    print("2. Change language")
    print("3. Exit Game")
    choice = input("Choice: ")

    if choice == "1":
        clear_screen()
        start_game()
    elif choice == "3":
        sys.exit(0)
    else:
        print("Invalid input")
        wait()

def main():
    main_menu()

if __name__ == "__main__":
    main()