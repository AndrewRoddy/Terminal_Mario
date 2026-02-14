from pynput import keyboard
import time
import csv
from copy import deepcopy
import random
import math
import sys

# Run this program in the atom IDE for the best results. Press f5 to run program :)

# Used to get the current key the keyboard is pressing
def get_key(framerate=0.367):
    # Does not allow the framerate under 0.2
    if framerate < 0.2:
        framerate = 0.2

    # Sets the Framerate
    time.sleep(framerate - 0.2)

    # Runs the keyboard key check
    with keyboard.Events() as events:
        # Gets the key currently being pressed
        event = events.get(0.2)

        # Return None if no key pressed or not a Press event
        if event is None or not isinstance(event, keyboard.Events.Press):
            return None

        # Convert the key to the string format the rest of the code expects
        key = event.key
        if isinstance(key, keyboard.Key):
            return f"Key.{key.name}"
        elif isinstance(key, keyboard.KeyCode) and key.char is not None:
            return f"'{key.char}'"
        return None


# Used to get the csv file that the map is contained in as a list
def get_map(level=1):
    # The level parameter sets the level

    # Imports the csv library to help read the csv file
    import csv

    # Creats a list of the maps
    map_list = ["maps/1-1.csv"]

    # Creates an empty map that the csv can be read to
    map = []

    # Opens the map file selected
    with open(map_list[level - 1]) as file:
        # Opens the reader for the csv file
        reader = csv.reader(file)

        # Append the data from the lines to the list
        for line in reader:
            map.append(line)

    # Return the map
    return map


def get_enemies(level=1):

    # Imports csv library
    import csv

    # A list of the available worlds' enemy lists
    enemy_list = ["enemy_list/e1-1.csv"]

    # Creates an empty list of enemies
    enemies = []

    # Opens the enemy_list file
    with open(enemy_list[level - 1]) as file:

        # Uses csv reader to read the file
        reader = csv.reader(file)

        # For every line in reader append the values as strings or integers
        for line in reader:
            enemies.append([line[0], int(line[1]), int(line[2])])

    # Return the list of enemies
    return enemies


# Used to print the map to the console
def print_map(map, x, y):
    # The left side of the printed map is x - 15
    l_x = x - 15

    # If the right side of the map is going to hit the right barrier then dont print it
    if l_x >= len(map[0]) - 30:
        r_x = l_x + 30
        l_x = len(map[0]) - 30

    # Mape sure the left side of the map is printed correctly
    if l_x < 1:
        l_x = 0
    r_x = l_x + 30

    # Build the entire frame as a single string to avoid flicker
    lines = ["\n"]

    # Top horizontal lines
    lines.append("  " + "_ " * (r_x - l_x) + " ")

    # Map rows
    for i in range(len(map)):
        lines.append("|" + " ".join(map[i][j] for j in range(l_x, r_x)) + " |")

    print("\n".join(lines))


# Used to allow the player to move left and right
def player_movement(map, key, x, y):
    # When the d or right key is pressed
    if key == "'d'" or key == "Key.right":
        # If the player can move right
        if x < (len(map[0]) - 1) and (map[y][x + 1] == " " or map[y][x + 1] == "$"):
            # Move rights
            x += 1

            # Increase the score
            score.movement_increase(x)

    # If the a key or left key is pressed
    if key == "'a'" or key == "Key.left":
        # If the player can move left
        if x > 0 and map[y][x - 1] == " ":
            # Move left
            x -= 1

    # If the player is on the bottom tile (dead)
    if (len(map) - 1) == y:
        # Make game_over True
        game_over(True)

    # If the player is above air
    elif map[y + 1][x] == " ":
        # Lower the player one tile
        y += 1

    # Return x and y coordinates
    return x, y


# Used to allow the player to jump
def jump(map, key, x, y):
    # If the space key or up key is pressed
    if key == "Key.space" or key == "Key.up" or key == "'w'":
        # Try make sure the index exists
        try:
            # If the tile below the player is not air
            if map[y + 1][x] != " ":
                # Try four times to allow the player to jump
                for _ in range(4):
                    # If the y level is greater than 1
                    # Makes sure the player does not fly out of bounds
                    if y >= 1:
                        # If there is air above the player
                        if map[y - 1][x] == " ":
                            # Move the player up
                            y -= 1

                        # If there is a block above the player
                        elif map[y - 1][x] == "#":
                            # Replace the block with an X
                            map[y - 1][x] = "X"
                            break

                        # If there is a ? block above the player
                        elif map[y - 1][x] == "?":
                            # Increase the score
                            score.up_score()

                            # Replace it with an X
                            map[y - 1][x] = "X"
                            break

        # If the player is going out of bounds make game_over True
        except IndexError:
            game_over(True)

    # Return the map and the y coordinate of the player
    return map, y


# Checks if the game is over
def game_over(over=False):

    # Creates a global variable named g_over
    global g_over

    # If using a parameter and the parameter is True make the game over
    if over == True:
        g_over = True

    # If the parameter is not used return false until it is turned true

    # Checks if the variable exists
    try:
        if g_over == True:
            return True

    except:
        pass

    # Return False
    return False


# Runs the score object
class Score:

    # Istalizes the score and x variables as 0
    def __init__(self):
        self.score = 0
        self.x = 0

    # If printed as a string print the score variable
    def __str__(self):
        return str(self.score)

    # Increases the score by the parameter times 1000
    def up_score(self, points=1):
        self.score += points * 1000

    # For every time x increases, increase the score by 100
    def movement_increase(self, x):
        if x > self.x:
            self.score += (x - self.x) * 100
            self.x = x


# Runs the enemies on the map
class Enemy:

    # Instalizes the goomba as alive and randomly chooses if the goomba will begin looking left or right
    def __init__(self, type, gx, gy):
        self.alive = True
        self.goomba_x = gx
        self.goomba_y = gy
        self.facing_left = random.choice([True, False])

    # If printed as a string print the variables next to eachother
    def __str__(self):
        return f"{self.alive} {self.goomba_x} {self.goomba_y} {self.facing_left}"

    def goomba(self, map, px, py):
        # Checks if goomba is alive and in range of the player
        if self.alive == True and (
            abs(self.goomba_x - px) < 17 or (abs(self.goomba_x) < 30 and px < 15)
        ):
            # If the goomba is in range begin the goomba related processes
            if self.goomba_y == 12:
                self.alive = False

            # If the goomba can fall make it fall
            elif map[math.floor(self.goomba_y) + 1][math.floor(self.goomba_x)] == " ":
                self.goomba_y += 0.5
            else:

                # If the player is directly above the goomba kill the goomba
                if math.floor(self.goomba_x) == px and self.goomba_y - 1 == py:
                    self.alive = False
                    py -= 3

                # If the goomba is facing left and can move left move left
                if self.facing_left == True:
                    if (
                        map[math.floor(self.goomba_y)][math.floor(self.goomba_x - 1)]
                        == " "
                    ):
                        self.goomba_x -= 0.25

                    # If the goomba cant move left turn it around
                    else:
                        self.facing_left = False

                # If the goomba is facing right and can move right, move right
                if self.facing_left == False:
                    if (
                        map[math.floor(self.goomba_y)][math.floor(self.goomba_x + 1)]
                        == " "
                    ):
                        self.goomba_x += 0.25

                    # If it cant turn it around
                    else:
                        self.facing_left = True

            # If the player and the goomba are on the same coordinate, end the game
            if math.floor(self.goomba_x) == px and math.floor(self.goomba_y) == py:
                game_over(True)

            # Change the map variable to the goomba
            map[math.floor(self.goomba_y)][math.floor(self.goomba_x)] = "g"

        return py

def main():
    # X coordinate of the player
    x = 4

    # Sets the usual variables incase checked for
    y = 9

    # Sets the original user_input
    user_input = "_"

    # Sets the starting key
    key = "_"

    # Sets the global score variable
    global score
    score = Score()

    # Sets the enemies on the map

    enemies = get_enemies(1)
    enemy_list = []

    for i in range(len(enemies)):
        enemy_list.append("goomba" + str(i))
        enemy_list[i] = Enemy(enemies[i][0], enemies[i][1], enemies[i][2])

    # Runs the frames of the game
    original_map = get_map(1)

    # Clear terminal
    print("\x1b[2J\x1b[H")    

    while game_over() == False:
        # Creates a copy of the map that can be easily edited
        map = deepcopy(original_map)

        # The get_key parameter sets the framerate of the game
        user_input = get_key(0.367)
        if user_input is None:
            key = "_"
        else:
            key = user_input

        # Allows the Player to Move
        x, y = player_movement(map, key, x, y)

        # If the user presses the space key allow the player to jump
        original_map, y = jump(original_map, key, x, y)

        for i in range(len(enemy_list)):
            y = enemy_list[i].goomba(map, x, y)

        map[y][x] = "m"

        if(x >= 199):
            sys.exit(f"\n\nYou Win!! \n\nPress (Enter) to quit\n\n")

        # Prints the map
        sys.stdout.write("\x1b[H")
        print_map(map, x, y)
        print("Score: " + str(score))
    sys.exit(f"\n\nGame Over \n\nPress (Enter) to quit\n\n")


if __name__ == "__main__":
    main()
