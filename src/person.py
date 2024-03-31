from enum import Enum
from random import randint
from colors import person_colors
from memory import Memory

type_pk_to_type = {
    1: "Copycat",
    2: "Cheater",
    3: "Cooperator",
    4: "Grudger",
    5: "Detective",
    6: "Copykitten",
    7: "Simpleton",
    8: "Random",
}

type_to_color = {
    "Small Copycat": "Light Blue",
    "Normal Copycat": "Blue",
    "Large Copycat": "Dark Blue",
    "Small Cheater": "Light Teal",
    "Normal Cheater": "Teal",
    "Large Cheater": "Dark Teal",
    "Small Cooperator": "Light Pink",
    "Normal Cooperator": "Pink",
    "Large Cooperator": "Dark Pink",
    "Small Grudger": "Light Yellow",
    "Normal Grudger": "Yellow",
    "Large Grudger": "Dark Yellow",
    "Small Detective": "Light Orange",
    "Normal Detective": "Orange",
    "Large Detective": "Dark Orange",
    "Small Copykitten": "Light Tan",
    "Normal Copykitten": "Tan",
    "Large Copykitten": "Dark Tan",
    "Small Simpleton": "Light Green",
    "Normal Simpleton": "Green",
    "Large Simpleton": "Dark Green",
    "Small Random": "Light Purple",
    "Normal Random": "Purple",
    "Large Random": "Dark Purple",
}

color_to_type = {
    "Light Blue": "Small Copycat",
    "Blue": "Normal Copycat",
    "Dark Blue": "Large Copycat",
    "Light Teal": "Small Cheater",
    "Teal": "Normal Cheater",
    "Dark Teal": "Large Cheater",
    "Light Pink": "Small Cooperator",
    "Pink": "Normal Cooperator",
    "Dark Pink": "Large Cooperator",
    "Light Yellow": "Small Grudger",
    "Yellow": "Normal Grudger",
    "Dark Yellow": "Large Grudger",
    "Light Orange": "Small Detective",
    "Orange": "Normal Detective",
    "Dark Orange": "Large Detective",
    "Light Tan": "Small Copykitten",
    "Tan": "Normal Copykitten",
    "Dark Tan": "Large Copykitten",
    "Light Green": "Small Simpleton",
    "Green": "Normal Simpleton",
    "Dark Green": "Large Simpleton",
    "Light Purple": "Small Random",
    "Purple": "Normal Random",
    "Dark Purple": "Large Random",
}


class Strategy(Enum):
    cooperate = 0
    defect = 1


class Person:

    def __init__(self, simulation, name, pk, location, memory):
        self.simulation = simulation
        self.name = name
        self.pk = pk
        self.age = randint(10, 61)
        # this effects how the person will do in a fight
        self.strength = randint(1, 3)
        # how many blocks can the person move in one turn
        self.speed = randint(1, 3)
        # how many blocks can the person see
        self.vision = randint(1, 3)
        # how likely the person is to panic
        self.fear = randint(1, 10)
        # where the person is located (1, 1, 1)
        # (floor, x, y)
        self.location = location
        # how many turns the person has been lost
        self.lost_counter = 0
        # how many turns the person has won
        self.won_counter = 0
        # how much health the person has if the person's health reaches 0, the person dies
        self.health = 100

        self.is_follower = randint(0, 1) == 0

        self.memory = memory

        self.type_pk = randint(1, 8)
        if self.strength > 3:
            extra = "Large"
        elif self.strength > 2:
            extra = "Normal"
        else:
            extra = "Small"
        self.type = f"{extra} " + type_pk_to_type[self.type_pk]
        self.color_title = type_to_color[self.type]
        self.color = person_colors[self.color_title]
        if self.fear > 5:
            self.strategy = Strategy.defect
        else:
            self.strategy = Strategy.cooperate

    def switch_strategy(self):
        if self.strategy == Strategy.defect:
            self.strategy = Strategy.cooperate
        else:
            self.strategy = Strategy.defect

    def __str__(self):
        return f"{self.name} is a {self.color_title} {self.type} {self.strategy} with {self.health} health at {self.location}."

    def is_dead(self):
        is_dead = False
        if self.health <= 0:
            is_dead = True
        return is_dead

    def move(self):
        for i in range(self.speed):
            what_is_around = self.look_around()
            self.memory.combine(what_is_around)
            self.move_one_block()

    def move_one_block(self):
        # TODO write a function to move the person one block

        # if the persons fear is greater than 5 they should move away from the closest fire
        # if the persons fear is a 10 they should jump out the closest window
        # if the persons fear is a 1 they should move towards the closest person

        # if the person is a follower they should move towards the closest person
        # if the person is a loner they should do their own thing

        # if the person is on the same floor as an exit they know about they should move towards the exit
        # if the person is on the same floor as a stair they know about they should move towards the stair
        # if the person is on the same floor as a door they know about they should move towards the door

        # the person should move to the closest wall if they are not near any of the above.
        #   Once they reach the wall they should move to along the wall

        # if the person knows nothing about their surroundings they should move randomly

        pass

    def move_to(self, location):
        if self.is_one_away(self.location, location):
            self.location = location
        else:
            raise Exception("You can only move one block at a time")

    @staticmethod
    def is_one_away(location1, location2):
        if location1[0] != location2[0]:
            return False
        if abs(location1[1] - location2[1]) > 1:
            return False
        if abs(location1[2] - location2[2]) > 1:
            return False
        return True

    def get_closest(self, lst):
        closest = lst[0]
        for location in lst:
            d1 = self.distance(location)
            d2 = self.distance(closest)
            if d1 is None or d2 is None:
                continue
            if d1 < d2:
                closest = location
        return closest

    def distance(self, location):
        if location is None:
            return None
        if self.location[0] != location[0]:
            return None
        x1 = self.location[1]
        y1 = self.location[2]
        x2 = location[1]
        y2 = location[2]
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    def look_around(self):
        what_is_around = Memory()
        blocked = []
        floor = self.location[0]
        x = self.location[1]
        y = self.location[2]
        for i in range(-(self.vision-1), self.vision):
            for j in range(-self.vision, self.vision + 1):
                if self.is_continue(i, j, x, y, floor, blocked):
                    continue
                self.search((floor, x + i, y + j), what_is_around, blocked)
        return what_is_around

    def is_continue(self, i, j, x, y, floor, blocked):
        if i == j:
            return True
        if x + i > len(self.simulation.building.text_building[floor][0]) or y + i > len(self.simulation.building.text_building[floor]):
            return True
        if self.is_blocked(blocked, x, y, i, j):
            return True
        return False

    def search(self, start_location, what_is_around, blocked):
        floor = start_location[0]
        x = start_location[1]
        y = start_location[2]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.is_continue(i, j, x, y, floor, blocked):
                    continue
                self.add_item(blocked, floor, i, j, what_is_around, x, y)

    def add_item(self, blocked, floor, i, j, what_is_around, x, y):
        location = (floor, x + i, y + j)
        if self.simulation.__is_wall(location):
            what_is_around.add("walls", location)
            if not self.is_diagonal(i, j):
                blocked.append((x + i, y + j, self.get_letter(i, j)))
        elif self.simulation.__is_door(location):
            what_is_around.add("doors", location)
        elif self.simulation.__is_exit(location):
            what_is_around.add("exits", location)
        elif self.simulation.__is_stair(location):
            what_is_around.add("stairs", location)
        elif self.simulation.__is_glass(location):
            what_is_around.add("glasses", location)
        elif self.simulation.__is_obstacle(location):
            what_is_around.add("obstacles", location)
        elif self.simulation.__is_empty(location):
            what_is_around.add("empties", location)
        elif (floor, x + i, y + j) in self.simulation.fire_locations:
            what_is_around.add("fires", location)
        elif self.simulation.__is_person(location):
            what_is_around.add("people", location)
        else:
            raise Exception("I see a char you didnt tell me about")

    def is_blocked(self, blocked, x, y, i, j):
        left = 0
        top = 0
        right = len(self.simulation.building.text_building[0])
        bottom = len(self.simulation.building.text_building)
        for block in blocked:
            b_x = block[0]
            b_y = block[1]
            letter = block[2]
            if y + j == b_y or x + i == b_x:
                if letter == 'l':
                    for k in range(left, b_x):
                        if x + i == k:
                            return True
                elif letter == 'r':
                    for k in range(b_x, right):
                        if x + i == k:
                            return True
                elif letter == 'd':
                    for k in range(b_y, bottom):
                        if y + j == k:
                            return True
                elif letter == 'u':
                    for k in range(top, b_y):
                        if y + j == k:
                            return True
            return False

    @staticmethod
    def is_diagonal(i, j):
        return i < 0 < j or j < 0 < i or (i < 0 and j < 0) or (i > 0 and j > 0)

    @staticmethod
    def get_letter(i, j):
        if i == 0 and j == 1:
            return 'u'
        if i == 0 and j == -1:
            return 'd'
        if i == 1 and j == 0:
            return 'r'
        if i == -1 and j == 0:
            return 'l'
        else:
            raise Exception('invalid coordinates')

    def combat(self, other):
        payoffs = self.__normal_form_game(other)
        person1_payoff = payoffs[0]
        person2_payoff = payoffs[1]
        if person1_payoff > person2_payoff:
            other.health -= 5
            # TODO move person1 into the spot
        elif payoffs[0] < payoffs[1]:
            self.health -= 5
            # TODO move person2 into the spot
        else:
            self.health -= 5
            other.health -= 5
            # TODO move no one

    def __normal_form_game(self, other):
        # TODO adjust the payoffs based on the persons strength levels
        base_payoffs = {
            (Strategy.cooperate, Strategy.cooperate): (3, 3),
            (Strategy.cooperate, Strategy.defect): (0, 5),
            (Strategy.defect, Strategy.cooperate): (5, 0),
            (Strategy.defect, Strategy.defect): (1, 1),
        }
        return base_payoffs[(self.strategy, other.strategy)]
