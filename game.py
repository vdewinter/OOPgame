import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
Round = 1

######################

GAME_WIDTH = 9
GAME_HEIGHT = 9

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class Gem(GameElement):
    SOLID = False   

    def __init__(self, color):
        self.color = color
        if self.color == "orange":
            self.IMAGE = "OrangeGem"
        if self.color == "blue":
            self.IMAGE = "BlueGem"

    def interact(self, player):
        if self.color == "orange":
            player.inventory.append("orange_gem")
        if self.color == "blue":
            player.inventory.append("blue_gem")
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

class Key(GameElement):

    IMAGE = "Key"
    SOLID = False

    def interact(self, player):
        player.inventory.append("key")
        GAME_BOARD.draw_msg("You just acquired a key! Open the door next.")

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True

    def interact(self, player):
        if "blue_gem" in player.inventory and "orange_gem" in player.inventory:
            self.SOLID = False
            GAME_BOARD.draw_msg("You opened the chest! Go finish the game.")   

class Star(GameElement):
    IMAGE = "Star"
    SOLID = False

    def interact(self, player):
        player.inventory.append("Star")
        GAME_BOARD.draw_msg("You got the Star! You have won the game!")
        increase_round(Round)
        initialize2()       

class Character(GameElement):
    IMAGE = "Girl"
    SOLID = True

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
        
    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

class Computer(GameElement):
    IMAGE = "Horns"
    SOLID = True

class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

    def interact(self, player):
        if "key" in player.inventory:
            self.SOLID = False
            GAME_BOARD.draw_msg("You opened the door!")

class Axe(GameElement):
    IMAGE = "Axe"
    SOLID = False

    def interact(self, player):
        player.inventory.append("axe")
        GAME_BOARD.draw_msg("You just acquired an axe! Chop down the tree.")

class Tree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

    def interact(self, player):
        if "axe" in player.inventory:
            self.SOLID = False
            GAME_BOARD.draw_msg("You cut down the tree!")

class Princess(GameElement):
    IMAGE = "Princess"
    SOLID = True

    def interact(self, player):
        if "orange_gem" in player.inventory:
            self.SOLID = False
            GAME_BOARD.draw_msg("You bribed the Princess in letting you pass!")

class CatTreat(GameElement):
    IMAGE = "Cat_Treat"
    SOLID = False

    def interact(self, player):
        player.inventory.append("Cat_Treat")
        GAME_BOARD.draw_msg("You just acquired a cat treat!")

class CuteCat(GameElement):
    IMAGE = "CuteCat"
    SOLID = True

    def interact(self, player):
        if "Cat_Treat" in player.inventory:
            self.SOLID = False
            GAME_BOARD.draw_msg("You have given the kitten a treat! Now it will let you through")

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    #Rock Positions
    rock_positions = [
        (0,0),
        (0,1),
        (0,2),
        (1,0),
        (1,4),
        (2,0),
        (2,2),
        (2,4),
        (2,6),
        (2,7),
        (3,2),
        (3,4),
        (3,7),
        (4,1),
        (4,2),
        (4,4),
        (4,5),
        (4,6),
        (4,7),
        (5,1),
        (6,1),
        (6,3),
        (6,5),
        (6,7),
        (7,1),
        (7,2),
        (7,3),
        (7,5),
        (7,6),
        (7,7),
        (7,8),
        (8,1),
        (4,8)
    ]
    wall_positions = [
        (0,8),
        (0,7)
    ]

    #Rocks
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[1], pos[0], rock)

    #Wall
    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[1], pos[0], wall)

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 8, PLAYER)
    print PLAYER

    #Message from Sponsors
    GAME_BOARD.draw_msg("Goal: get the star.")

    #Gems
    orange_gem = Gem("orange")
    GAME_BOARD.register(orange_gem)
    GAME_BOARD.set_el(6, 3, orange_gem)

    blue_gem = Gem("blue")
    GAME_BOARD.register(blue_gem)
    GAME_BOARD.set_el(8, 6, blue_gem)

    #Keys
    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(0, 7, key)

    #Cat Treat
    cat_treat = CatTreat()
    GAME_BOARD.register(cat_treat)
    GAME_BOARD.set_el(2, 6, cat_treat)

    #Axe
    axe = Axe()
    GAME_BOARD.register(axe)
    GAME_BOARD.set_el(0, 3, axe)

    #Chest
    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(6, 8, chest)

    #Door
    door = Door()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(0, 6, door)

    #Tree
    tree = Tree()
    GAME_BOARD.register(tree)
    GAME_BOARD.set_el(1, 2, tree)

    #Princess
    princess = Princess()
    GAME_BOARD.register(princess)
    GAME_BOARD.set_el(3, 4, princess)

    #Cat
    cute_cat = CuteCat()
    GAME_BOARD.register(cute_cat)
    GAME_BOARD.set_el(5, 5, cute_cat)

    #Prize
    star = Star()
    GAME_BOARD.register(star)
    GAME_BOARD.set_el(8, 8, star)

def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    elif KEYBOARD[key.RIGHT]:
        direction = "right"
    elif KEYBOARD[key.LEFT]:
        direction = "left"
    elif KEYBOARD[key.DOWN]:
        direction = "down"

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)

def increase_round(Round):
    new_round = Round + 1
    for x in range(GAME_WIDTH):
        for y in range(GAME_HEIGHT):
            GAME_BOARD.del_el(x,y)
    return new_round

def initialize2():
    star_pos = [
        (0,0),
        (0,1),
        (0,2),
        (1,0),
        (1,4),
        (2,0),
        (2,2),
        (2,4),
        (2,6),
        (2,7),
        (3,2),
        (3,4),
        (3,7),
        (4,1),
        (4,2),
        (4,4),
        (4,5),
        (4,6),
        (4,7),
        (5,1),
        (6,1),
        (6,3),
        (6,5),
        (6,7),
        (7,1),
        (7,2),
        (7,3),
        (7,5),
        (7,6),
        (7,7),
        (7,8),
        (8,1),
        (4,8)
    ]

    for pos in star_pos:
        star = Star()
        GAME_BOARD.register(star)
        GAME_BOARD.set_el(pos[1], pos[0], star)

    global COMPUTER
    COMPUTER = Computer()
    GAME_BOARD.register(COMPUTER)
    GAME_BOARD.set_el(8,0, COMPUTER)
    GAME_BOARD.draw_msg("Congratulations.")