from pynput import keyboard
import time
import re
import csv
from copy import deepcopy
import random
import math
# Run this program in the atom IDE for the best results. Press f5 to run program :)

# Used to get the current key the keyboard is pressing
def get_key(framerate=0.367):

    # Does not allow the framerate under 0.2
    if framerate < 0.2:
        framerate = 0.2

    # Sets the Framerate
    time.sleep(framerate-0.2)

    # Runs the keyboard key check
    with keyboard.Events() as events:

        # Gets the key currently being pressed
        event = events.get(0.2)

        # Returns the key currently being pressed
        return event

# Used to get the csv file that the map is contained in as a list
def get_map(level=1):
    import csv
    map_list = ["1-1.csv"]
    map = []
    with open(map_list[level-1]) as file:
        reader = csv.reader(file)
        for line in reader:
            map.append(line)

    return map


def print_map(map, x, y):
    l_x = x - 15
    if l_x < 1:
        l_x = 0

    r_x = l_x + 30
    
    if r_x == len(map[0]) - 1:
        r_x = len(map) - 1
        l_x = r_x - 30
    
    for i in range(len(map)):
        print("||", end="")
        for j in range(l_x, r_x):
            print(map[i][j], end=" ")
        print("||")
    #print("Coins: " + str(coins))


def player_movement(map, key, x, y):
    if key == "'d'" or key == "Key.right":
        if x < (len(map[0])-1) and map[y][x+1] == " ":
            x += 1
    if key == "'a'" or key == "Key.left":
        if x > 0 and map[y][x-1] == " ":
            x -= 1

    if map[y+1][x] == " ":
        y += 1

    return x, y


def jump(map, key, x, y):
    if key == "Key.space" or key == "Key.up":
        if map[y+1][x] != " ":
            for _ in range(4):
                if y >= 1:
                    if map[y-1][x] == " ":
                        y -= 1
                    elif map[y-1][x] == "#":
                        map[y-1][x] = "X"
    return map, y


class Enemy:
    
    def __init__(self, gx, gy):
        
        self.alive = True
        self.goomba_x = gx
        self.goomba_y = gy
        self.facing_left = random.choice([True, False])
        """
        self.goomba_y = y
        choice = random.randint(2)
        if choice == 1:
            self.going_left = True  
        if choice == 2:
            self.going_left = False  
        """   
    """
    @property
    def goomba_x(self):
        return self._x

    @goomba_x.setter
    def goomba_x(self, goomba_x):
        self._goomba_x = goomba_x
    """
    def goomba(self, map, px, py):
        
        # Checks if goomba is alive
        if self.alive == True:
            
            if math.floor(self.goomba_x) == px and self.goomba_y - 1 == py:
                self.alive = False
                
            if self.facing_left == True:
                if map[self.goomba_y][math.floor(self.goomba_x - 1)] == " ":
                    self.goomba_x -= 0.25
                else:
                    self.facing_left = False
            
            if self.facing_left == False:
                if map[self.goomba_y][math.floor(self.goomba_x + 1)] == " ":
                    self.goomba_x += 0.25
                else:
                    self.facing_left = True
            map[self.goomba_y][math.floor(self.goomba_x)] = "G"
            
            # Checks if the player has landed on the goomba
            
        

        return map

def main():

    # X coordinate of the player
    x = 0
    # Sets the usual variables incase checked for
    y = 9
    user_input = "_"
    key = "_"

    goomba_1 = Enemy(22, 10)


    # Runs the frames of the game
    original_map = get_map(1)
    while True:
        map = deepcopy(original_map)
        
        
        
        
        # The get_key parameter sets the framerate of the game
        user_input = get_key(0.367)
        if user_input == None:
            key = "_"
        else:
            if grouper := re.search(r"key=(.+)\)", str(user_input)):
                key = grouper.group(1)




        # Allows the Player to Move
        x, y = player_movement(map, key, x, y)

        # If the user presses the space key allow the player to jump
        original_map, y = jump(original_map, key, x, y)
        
        map[y][x] = "p" 
        goomba_1.goomba(map, x, y)
        #map(goomba_movement(1)[0], goomba_movement(1)[1])
        # Prints the map
        print_map(map, x, y)

if __name__ == "__main__":
    main()