from enum import Enum
from random import randint
from colors import person_colors
from memory import Memory
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from prompt import get_choice_from_AI, get_random_choice


class Strategy(Enum):
    cooperate = 0
    defect = 1


class Person:

    def __init__(self, simulation, name, pk, location, memory, verbose=False):
        self.verbose = verbose
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
        self.fear = randint(0, 10)
        # where the person is located (1, 1, 1)
        # (floor, x, y)
        self.location = location

        self.room_type = None

        # how much health the person has if the person's health reaches 0, the person dies
        self.health = 100

        self.is_follower = randint(0, 1) == 0

        if self.is_follower:
            self.color_title = "Yellow"
            self.color = person_colors["Yellow"]
        else:
            self.color_title = "Blue"
            self.color = person_colors["Blue"]

        self.memory = memory

        self.type_pk = randint(1, 8)

        if self.fear > 5:
            self.strategy = Strategy.defect
        else:
            self.strategy = Strategy.cooperate

        self.end_turn_in_fire = True

    def switch_strategy(self):
        if self.strategy == Strategy.defect:
            self.strategy = Strategy.cooperate
        else:
            self.strategy = Strategy.defect

    def __str__(self):
        return f"{self.name} is a {self.color_title} {self.strategy} with {self.health} health at {self.location}."

    def is_dead(self):
        is_dead = False
        if self.health <= 0:
            is_dead = True
        return is_dead

    def move(self):
        other = None
        for i in range(self.speed):
            if self.is_dead():
                break
            what_is_around = self.look_around()
            self.memory.combine(what_is_around)
            other = self.move_one_block()
            # hit person
            if other:
                break
            # in a fire
            if self.location in self.simulation.fire_locations:
                self.health -= 25
                self.end_turn_in_fire = True
            else:
                self.end_turn_in_fire = False
            # at a stair
            if self.simulation.__is_stair(self.location):
                self.location = (self.location[0] - 1, self.location[1], self.location[2])

        return other

    def move_one_block(self):
        options = self.get_options_for_AI()
        if self.simulation.with_ai:
            situation = self.get_situation_for_AI()
            temperature = self.get_temperature_for_AI()
            choice = get_choice_from_AI(situation, options, temperature)
        else:
            choice = get_random_choice(options)
        return self.make_choice(choice)

    def make_choice(self, choice):
        if choice is None:
            raise Exception("AI did not give a valid choice")
        if choice == 'A':
            return self.explore()
        elif choice == 'B':
            return self.move_randomly()
        elif choice == 'C':
            closest_person = self.get_closest(self.memory.people)
            return self.move_towards(closest_person)
        elif choice == 'D':
            closest_door = self.get_closest(self.memory.doors)
            return self.move_towards(closest_door)
        elif choice == 'E':
            closest_glass = self.get_closest(self.memory.glasses)
            return self.move_towards(closest_glass)
        elif choice == 'F':
            closest_fire = self.get_closest(self.memory.fires)
            return self.move_towards(closest_fire)
        elif choice == 'G':
            closest_glass = self.get_closest(self.memory.glasses)
            if not self.break_glass(closest_glass):
                raise Exception("Cant break glass unless you are near it")
            return None
        elif choice == 'H':
            closest_person = self.get_closest(self.memory.people)
            return self.move_towards(closest_person)
        elif choice == 'I':
            closest_door = self.get_closest(self.memory.doors)
            return self.move_towards(closest_door)
        elif choice == 'J':
            closest_glass = self.get_closest(self.memory.broken_glass)
            if not self.jump_out_of_window(closest_glass):
                raise Exception("Cant jump out of window unless you are near it")
            return None
        elif choice == 'K':
            return self.follow_evacuation_plan()
        elif choice == 'L':
            closest_exit = self.get_closest(self.memory.exits)
            return self.move_towards(closest_exit)
        elif choice == 'M':
            closest_stair = self.get_closest(self.memory.stairs)
            return self.move_towards(closest_stair)
        elif choice == 'N':
            return None
        else:
            raise Exception("Invalid choice")

    def get_temperature_for_AI(self):
        if self.fear >= 5:
            return 0.7
        else:
            return 0.3

    def get_situation_for_AI(self):
        situation = \
            f"""
            Do you like people: {self.is_follower}
            Floor: {self.location[0]}
            Strength: {self.strength}
            Health: {self.health}
            Fear: {self.fear}
            Nearest Exit: {self.get_closest(self.memory.exits)}
            Nearest Stairs: {self.get_closest(self.memory.stairs)}
            Nearest Person: {self.get_closest(self.memory.people)}
            Nearest Window: {self.get_closest(self.memory.glasses)}
            Nearest Fire: {self.get_closest(self.memory.fires)}
            People Near: {self.get_number_of_people_near()}
            Know Evacuation Plan: {self.memory.evacuation_plan}
            Time to Get Out: {self.get_time_to_get_out()}
            Room Type: {self.get_room_type()}
            """
        return situation

    def get_options_for_AI(self):
        # dont have to return all of these but here is the idea
        # option A: explore | always open
        # option B: move randomly | always open
        # option C: move towards a person | if know about person, more likely if you like people
        # option D: move towards a door | if know about door
        # option E: move towards a glass | if know about glass
        # option F: move towards a fire | if know about fire and stuck in room
        # option G: break glass | if next to glass
        # option H: fight someone for a spot | if someone is in a spot you want
        # option I: run through fire to safety | if stuck in room
        # option J: jump out of building | if next to
        # option K: follow evacuation plan | if know about evacuation plan
        # option L: move to exit | if know about exit on your floor
        # option M: move to stair | if know about stair on your floor
        # option N: do nothing | always open
        options = ["A", "B", "N"]
        if self.memory.exits:
            options.append("L")
        if self.memory.stairs:
            options.append("M")
        if self.memory.people:
            options.append("C")
            if self.is_next_to(self.memory.people):
                options.append("H")
        if self.memory.doors:
            options.append("D")
        if self.memory.glasses:
            options.append("E")
            if self.can_break_glass() and self.is_next_to(self.memory.glasses):
                options.append("G")
        if self.memory.fires:
            options.append("F")
        if self.memory.broken_glass and self.is_next_to(self.memory.broken_glass):
            options.append("J")
        if self.memory.evacuation_plan:
            options.append("K")
        if self.is_next_to(self.memory.fires):
            options.append("I")
        options.sort()
        return options

    def get_time_to_get_out(self):
        long_time = -1
        closest_exit = self.get_closest(self.memory.exits)
        if closest_exit:
            d = self.get_distance(closest_exit) 
            if not d:
                return long_time
            number_of_people = self.get_number_of_people_near()
            return number_of_people + d
        return long_time

    def is_next_to(self, lst):
        for location in lst:
            if self.is_one_away(self.location, location):
                return True
        return False

    def follow_evacuation_plan(self):
        # TODO write a function that will allow the person to follow the evacuation plan
        # With how the floors are set up potenially we could have them find the closest "p" to the right of them. With the exception of floor 1. 
        closest_exit_plan = self.get_closest(self.memory.exit_plans)
        closest_exit = self.get_closest_from_p(closest_exit_plan, self.simulation.building.object_locations["exit"])
        return self.move_towards(closest_exit)

    def explore(self):
        if "room" == self.room_type:
            closest_door = self.get_closest(self.memory.doors)
            if closest_door:
                return self.move_towards(closest_door)
        furthest_wall = self.get_furthest(self.memory.walls)
        if furthest_wall:
            return self.move_towards(furthest_wall)
        return self.move_randomly()
    
    def move_randomly(self):
        x = randint(-1, 1)
        y = randint(-1, 1)
        new_location = (self.location[0], self.location[1] + x, self.location[2] + y)
        return self.move_to(new_location)

    def move_towards(self, location):
        if location is None:
            return None
        floor1 = self.location[0]
        floor2 = location[0]
        if floor1 != floor2:
            return None
        n_x = None
        n_y = None
        for tries in range(2):
            path = self.get_path(floor1, location, tries)
            if len(path) != 0:
                n_x, n_y = path[1]
                break
        if n_x is None or n_y is None:
            return None
        new_location = (floor1, n_x, n_y)
        return self.move_to(new_location)

    def get_path(self, floor1, location, tries):
        grid = self.get_grid(floor1, tries)
        x1 = self.location[1]
        y1 = self.location[2]
        start = grid.node(x1, y1)
        x2 = location[1]
        y2 = location[2]
        end = grid.node(x2, y2)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, grid)
        if self.verbose:
            print('operations:', runs, 'path length:', len(path))
            print(grid.grid_str(path=path, start=start, end=end))
        return path

    def get_grid(self, floor1, tries):
        temp_grid = self.simulation.building.grid[floor1]
        if tries == 0:
            # try with moving around people (collisions are not allowed)
            for row in range(len(temp_grid)):
                for col in range(len(temp_grid[row])):
                    if temp_grid[row][col] == -1:
                        temp_grid[row][col] = 0
        else:
            # try without moving around people (collisions are allowed)
            for row in range(len(temp_grid)):
                for col in range(len(temp_grid[row])):
                    if temp_grid[row][col] == -1:
                        temp_grid[row][col] = 1
        grid = Grid(matrix=temp_grid)
        return grid

    def break_glass(self, glass_location):
        if self.is_one_away(self.location, glass_location):
            if self.can_break_glass():
                # the person breaks the glass and hurts themselves doing it
                self.simulation.building.text_building[glass_location[0]][glass_location[1]][glass_location[2]] = 'b'
                self.memory.add("broken_glass", glass_location)
                self.health -= 25
            else:
                # too weak to break the glass, but they still hurt themselves trying
                self.health -= 5
            return True
        return False

    def jump_out_of_window(self, broken_glass_location):
        if self.is_one_away(self.location, broken_glass_location):
            floor = self.location[0]
            # hurt self on broken glass
            self.health -= randint(0, 10)
            if floor == 2:
                # hurt self on the way down
                self.health -= randint(10, 30)
            elif floor == 3:
                # hurt self on the way down
                self.health -= randint(30, 50)
            elif floor > 3:
                # hurt self on the way down
                self.health -= randint(50, 100)
            self.move_to(broken_glass_location)
            return True
        return False

    def can_break_glass(self):
        if self.strength > 2:
            return True
        return False

    def move_to(self, location):
        if self.is_one_away(self.location, location) and (
                self.simulation.__is_empty(location) or self.simulation.__is_exit(
                location) or self.simulation.__is_stair(location) or self.simulation.__is_person(location)):
            other = self.simulation.__is_person(location)
            if other is not None:
                return other
            self.location = location
            return None
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
        """
        get the closet of something from a list. ex: get the closest wall, get the closest person, etc.
        """
        if len(lst) == 0:
            return None
        closest = lst[0]
        for location in lst:
            d1 = self.get_distance(location)
            d2 = self.get_distance(closest)
            if d1 is None or d2 is None:
                continue
            if d1 < d2:
                closest = location
        return closest

    def get_furthest(self, lst):
        """
        get the furthest of something from a list. ex: get the furthest wall, get the furthest person, etc.
        """
        if len(lst) == 0:
            return None
        furthest = lst[0]
        for location in lst:
            d1 = self.get_distance(location)
            d2 = self.get_distance(furthest)
            if d1 is None or d2 is None:
                continue
            if d1 > d2:
                furthest = location
        return furthest

    def get_distance(self, location):
        if location is None:
            return None
        if self.location[0] != location[0]:
            return None
        x1 = self.location[1]
        y1 = self.location[2]
        x2 = location[1]
        y2 = location[2]
        return (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5
    
    def get_closest_from_p(self, p, lst):
        """
        get the closet of something from a list. ex: get the closest wall, get the closest person, etc.
        """
        if len(lst) == 0:
            return None
        closest = lst[0]
        for location in lst:
            d1 = self.get_distance_from_p(p, location)
            d2 = self.get_distance_from_p(p, closest)
            if d1 is None or d2 is None:
                continue
            if d1 < d2:
                closest = location
        return closest
    
    @staticmethod
    def get_distance_from_p(p, location):
        if location is None:
            return None
        if p[0] != location[0]:
            return None
        x1 = p[1]
        y1 = p[2]
        x2 = location[1]
        y2 = location[2]
        return (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5

    def look_around(self):
        what_is_around = Memory()
        blocked = []
        floor = self.location[0]
        x = self.location[1]
        y = self.location[2]
        for i in range(-(self.vision - 1), self.vision):
            for j in range(-self.vision, self.vision + 1):
                if self.is_continue(i, j, x, y, floor, blocked):
                    continue
                self.search((floor, x + i, y + j), what_is_around, blocked)
        return what_is_around

    def is_continue(self, i, j, x, y, floor, blocked):
        if i == j:
            return True
        if x + i > len(self.simulation.building.text_building[floor][0]) or y + i > len(
                self.simulation.building.text_building[floor]):
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
        elif location in self.simulation.fire_locations:
            what_is_around.add("fires", location)
        elif self.simulation.__is_person(location):
            what_is_around.add("people", location)
        elif self.simulation.__is_broken_glass(location):
            what_is_around.add("broken_glass", location)
        elif self.simulation.__is_room(location):
            self.room_type = "room"
        elif self.simulation.__is_hall(location):
            self.room_type = "hall"
        elif self.simulation.__is_exit_plan(location):
            what_is_around.add("exit_plans", location)
        else:
            raise Exception("I see a char you didn't tell me about")

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
        wanted_location = other.location
        not_wanted_location = self.location
        payoffs = self.__normal_form_game(other)
        person1_payoff = payoffs[0]
        person2_payoff = payoffs[1]
        if person1_payoff > person2_payoff:
            other.health -= 5
            if other.fear < 10:
                other.fear += 1
            if self.fear > 0:
                self.fear -= 1
            self.location = wanted_location
            other.location = not_wanted_location
        elif payoffs[0] < payoffs[1]:
            self.health -= 5
            if self.fear < 10:
                self.fear += 1
            if other.fear > 0:
                other.fear -= 1
        else:
            self.health -= 5
            other.health -= 5
            if self.fear < 10:
                self.fear += 1
            if other.fear < 10:
                other.fear += 1

    def __normal_form_game(self, other):
        # TODO adjust the payoffs based on the persons strength levels
        payoffs = {
            (Strategy.cooperate, Strategy.cooperate): (3, 3),
            (Strategy.cooperate, Strategy.defect): (0, 5),
            (Strategy.defect, Strategy.cooperate): (5, 0),
            (Strategy.defect, Strategy.defect): (1, 1),
        }
        return payoffs[(self.strategy, other.strategy)]

    def get_number_of_people_near(self, distance=5):
        count = 0
        for person in self.memory.people:
            if self.is_near(person.location, distance):
                count += 1
        return count

    def is_near(self, location, distance):
        d1 = self.get_distance(location)
        if d1 < distance:
            return True
