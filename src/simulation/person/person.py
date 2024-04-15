from random import randint
from src.simulation.colors import person_colors
from .memory import Memory
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from src.simulation.logger import setup_logger
from copy import deepcopy
from .strategy import Strategy
from .fight_entry import FightEntry
from .choice import Choice


class Person:

    def __init__(self,
                 simulation,
                 name,
                 pk,
                 location,
                 memory,
                 simulation_count,
                 verbose,
                 age,
                 strength,
                 speed,
                 visibility,
                 fear,
                 health,
                 is_follower,
                 familiarity,
                 personality,
                 personality_title
                 ):

        self.number_of_fights_won = 0
        self.number_of_fights_lost = 0
        self.number_of_fights_tied = 0
        self.number_of_fire_touches = 0
        self.number_of_max_fear = 0

        self.simulation = simulation
        self.name = name
        self.pk = pk
        self.age = age
        # this effects how the person will do in a fight
        self.strength = strength
        # how many blocks can the person move in one turn
        self.speed = speed
        # how many blocks can the person see
        self.visibility = visibility
        # how likely the person is to panic
        self.fear = fear
        # where the person is located (1, 1, 1)
        # (floor, x, y)
        self.location = location
        self.room_type = None
        # how much health the person has if the person's health reaches 0, the person dies
        self.health = health

        self.is_follower = is_follower
        self.familiarity = familiarity

        if self.is_follower:
            self.color_title = "Yellow"
            self.color = person_colors["Yellow"]
        else:
            self.color_title = "Blue"
            self.color = person_colors["Blue"]

        self.memory = memory

        self.end_turn_in_fire = True

        self.personality = personality
        self.personality_title = personality_title

        self.fight_history = []

        self.choice = Choice(self)

        self.logger = setup_logger("person_logger", f'../logs/run{simulation_count}/people/person{pk}.log',
                                   verbose)
        self.logger.info('This log is for INFO purposes from person')

        self.logger.info(f"name: {self.name}")
        self.logger.info(f"age: {self.age}")
        self.logger.info(f"age: {self.age}")
        self.logger.info(f"strength: {self.strength}")
        self.logger.info(f"speed: {self.speed}")
        self.logger.info(f"vision: {self.visibility}")
        self.logger.info(f"fear: {self.fear}")
        self.logger.info(f"health: {self.health}")
        self.logger.info(f"is_follower: {self.is_follower}")
        self.logger.info(f"location: {self.location}")
        self.logger.info(f"color_title: {self.color_title}")

    def statistics(self):
        stats = [
            f"{self.name} has won {self.number_of_fights_won} fights",
            f"{self.name} has lost {self.number_of_fights_lost} fights",
            f"{self.name} has tied {self.number_of_fights_tied} fights",
            f"{self.name} has touched fire {self.number_of_fire_touches} times",
            f"{self.name} has reached max fear {self.number_of_max_fear} times",
            f"{self.name} is a {self.color_title} person with {self.health} health and {self.strength} strength at {self.location}.",
        ]

        for stat in stats:
            self.logger.info(stat)

    def __str__(self):
        return f"{self.name} {self.personality_title} {self.color_title} {self.health} {self.location}."

    def is_dead(self):
        is_dead = False
        if self.health <= 0:
            is_dead = True
        return is_dead

    def move(self):
        self.logger.info(f"{self.name} is moving")
        self.logger.info(f"{self.name} is at {self.location}")
        if self.fear == self.simulation.max_fear:
            self.number_of_max_fear += 1
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
                self.number_of_fire_touches += 1
            else:
                self.end_turn_in_fire = False
            # at a stair
            if self.simulation.is_stair(self.location):
                self.location = (self.location[0] - 1, self.location[1], self.location[2])
        self.logger.info(f"{self.name} is at {self.location}")
        return other

    def move_one_block(self):
        choice, other = self.choice.make()
        if choice is None:
            raise Exception("did not give a valid choice")
        self.logger.info(f"{self.name} made choice {choice}")
        return other

    def get_time_to_get_out(self):
        long_time = -1
        closest_exit = self.get_closest(self.location, self.memory.exits)
        if closest_exit:
            d = self.get_distance(self.location, closest_exit)
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
        closest_exit_plan = self.get_closest(self.location, self.memory.exit_plans)
        closest_exit = self.get_closest(closest_exit_plan, self.simulation.building.object_locations["exits"])
        return self.move_towards(closest_exit)

    def explore(self):
        if self.is_in_room():
            closest_door = self.get_closest(self.location, self.memory.doors)
            if closest_door:
                return self.move_towards(closest_door)
        furthest_empty = self.get_furthest(self.location, self.memory.empties)
        if furthest_empty:
            return self.move_towards(furthest_empty)
        return self.move_randomly()

    def move_randomly(self):
        for i in range(8):
            x = randint(-1, 1)
            y = randint(-1, 1)
            new_location = (self.location[0], self.location[1] + x, self.location[2] + y)
            return self.move_to(new_location)
        return None

    def move_towards(self, location):
        if location is None:
            return None
        self.simulation.is_in_building(location)
        floor1 = self.location[0]
        floor2 = location[0]
        if floor1 != floor2:
            return None
        n_x = None
        n_y = None
        for i in range(4):
            grid = self.get_grid(i)
            path = self.get_path(location, grid)
            if path and len(path) >= 2:
                node = path[1]
                n_x = node.x
                n_y = node.y
                new_location = (floor1, n_x, n_y)
                if self.is_one_away(self.location, new_location):
                    break
                n_x = None
                n_y = None
        if n_x is None or n_y is None:
            return None
        new_location = (floor1, n_x, n_y)
        return self.move_to(new_location)

    def get_path(self, location, grid):
        if location is None:
            raise Exception("location is None")
        if grid is None:
            raise Exception("grid is None")
        if not self.simulation.is_in_building(self.location):
            raise Exception(f"location is not in building: {self.location}")
        if not self.simulation.is_in_building(location):
            raise Exception(f"location is not in building: {location}")
        for row in grid.nodes:
            for node in row:
                if node.weight == -3:
                    node.walkable = False
        x1 = self.location[1]
        y1 = self.location[2]
        start = grid.node(y1, x1)
        x2 = location[1]
        y2 = location[2]
        end = grid.node(y2, x2)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, grid)
        self.logger.info(f'operations:', runs, 'path length:', len(path))
        self.logger.info(grid.grid_str(path=path, start=start, end=end))
        return path

    def get_grid(self, i):
        floor = self.location[0]
        temp_grid = deepcopy(self.simulation.building.grid[floor])
        if i == 0:
            self.switcher(temp_grid, -3, -3)
        elif i == 1:
            self.switcher(temp_grid, 3, -3)
        elif i == 2:
            self.switcher(temp_grid, -3, 3)
        elif i == 3:
            self.switcher(temp_grid, 3, 3)
        else:
            raise Exception("invalid i")
        grid = Grid(matrix=temp_grid)
        return grid

    @staticmethod
    def switcher(temp_grid, p, f):
        for row in range(len(temp_grid)):
            for col in range(len(temp_grid[row])):
                if temp_grid[row][col] == -1:
                    temp_grid[row][col] = p
                elif temp_grid[row][col] == -2:
                    temp_grid[row][col] = f

    def break_glass(self, glass_location):
        if self.is_one_away(self.location, glass_location):
            if self.can_break_glass():
                # the person breaks the glass and hurts themselves doing it
                self.simulation.building.text_building[glass_location[0]][glass_location[1]][glass_location[2]] = 'b'
                self.memory.add("broken_glasses", glass_location)
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
            return self.move_to(broken_glass_location)
        return None

    def can_break_glass(self):
        if self.strength > 2:
            return True
        return False

    def move_to(self, location):
        self.simulation.is_in_building(location)
        if not self.is_one_away(self.location, location):
            raise Exception(f"location is not one away: {location}")
        if not self.simulation.is_valid_location_for_person(location):
            raise Exception(f"location is not valid: {location} {self.simulation.building.text_building[location[0]][location[1]][location[2]]}")
        other = self.simulation.is_person(location)
        if other is not None:
            return other
        self.location = location
        return None

    @staticmethod
    def is_one_away(location1, location2):
        if location1[0] != location2[0]:
            return False
        x = abs(location1[1] - location2[1])
        y = abs(location1[2] - location2[2])
        if x > 1 or y > 1:
            return False
        return True

    def get_closest(self, location1, lst):
        """
        get the closet of something from a list. ex: get the closest wall, get the closest person, etc.
        """
        if len(lst) == 0:
            return None
        closest = next(iter(lst))
        for location2 in lst:
            d1 = self.get_distance(location1, location2)
            d2 = self.get_distance(location1, closest)
            if d1 is None or d2 is None:
                continue
            if d1 < d2:
                closest = location2
        return closest

    def get_furthest(self, location1, lst):
        """
        get the furthest of something from a list. ex: get the furthest wall, get the furthest person, etc.
        """
        if len(lst) == 0:
            return None
        furthest = next(iter(lst))
        for location2 in lst:
            d1 = self.get_distance(location1, location2)
            d2 = self.get_distance(location1, furthest)
            if d1 is None or d2 is None:
                continue
            if d1 > d2:
                furthest = location2
        return furthest

    @staticmethod
    def get_distance(location1, location2):
        if location2 is None:
            return None
        if location1[0] != location2[0]:
            return None
        x1 = location1[1]
        y1 = location1[2]
        x2 = location2[1]
        y2 = location2[2]
        return (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5

    def look_around(self):
        what_is_around = Memory()
        blocked = []
        floor = self.location[0]
        x = self.location[1]
        y = self.location[2]
        # -1 from vision because the search function will look at the current location
        for i in range(-(self.visibility - 1), self.visibility):
            for j in range(-self.visibility, self.visibility + 1):
                if self.is_continue(i, j, x, y, blocked):
                    continue
                self.search((floor, x + i, y + j), what_is_around, blocked)
        return what_is_around

    def is_continue(self, i, j, x, y, blocked):
        if i == j:
            return True
        a = x + i
        b = y + j
        if 0 > a > self.simulation.building.row_count-1 or 0 > b > self.simulation.building.col_count-1:
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
                if self.is_continue(i, j, x, y, blocked):
                    continue
                self.add_to_memory(blocked, floor, i, j, what_is_around, x, y)

    def add_to_memory(self, blocked, floor, i, j, what_is_around, x, y):
        location = (floor, x + i, y + j)
        self.simulation.is_in_building(location)
        if self.simulation.is_wall(location):
            what_is_around.add("walls", location)
            if not self.is_diagonal(i, j):
                blocked.append((x + i, y + j, self.get_letter(i, j)))
        elif self.simulation.is_door(location):
            what_is_around.add("doors", location)
        elif self.simulation.is_exit(location):
            what_is_around.add("exits", location)
        elif self.simulation.is_stair(location):
            what_is_around.add("stairs", location)
        elif self.simulation.is_glass(location):
            what_is_around.add("glasses", location)
        elif self.simulation.is_obstacle(location):
            what_is_around.add("obstacles", location)
        elif self.simulation.is_empty(location):
            what_is_around.add("empties", location)
        elif location in self.simulation.fire_locations:
            what_is_around.add("fires", location)
        elif self.simulation.is_person(location):
            what_is_around.add("people", location)
        elif self.simulation.is_broken_glass(location):
            what_is_around.add("broken_glasses", location)
        elif self.simulation.is_room(location):
            self.room_type = "room"
        elif self.simulation.is_hallway(location):
            self.room_type = "hall"
        elif self.simulation.is_exit_plan(location):
            what_is_around.add("exit_plans", location)
        else:
            raise Exception(f"I see a char you didn't tell me about: {self.simulation.building.text_building[floor][x + i][y + j]}")

    def is_blocked(self, blocked, x, y, i, j):
        left = 0
        top = 0
        right = self.simulation.building.row_count
        bottom = self.simulation.building.col_count
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
            self.number_of_fights_won += 1
            other.number_of_fights_lost += 1
            other.health -= 5
            if other.fear < 10:
                other.fear += 1
            if self.fear > 0:
                self.fear -= 1
            self.location = wanted_location
            other.location = not_wanted_location
        elif payoffs[0] < payoffs[1]:
            self.number_of_fights_lost += 1
            other.number_of_fights_won += 1
            self.health -= 5
            if self.fear < 10:
                self.fear += 1
            if other.fear > 0:
                other.fear -= 1
        else:
            self.number_of_fights_tied += 1
            other.number_of_fights_tied += 1
            self.health -= 5
            other.health -= 5
            if self.fear < 10:
                self.fear += 1
            if other.fear < 10:
                other.fear += 1

    def get_age_group(self):
        if 0 < self.age < 10:
            return -2
        elif 9 < self.age < 19:
            return -1
        elif 18 < self.age < 36:
            return 1
        elif 35 < self.age < 51:
            return 0
        elif 50 < self.age < 81:
            return -1
        else:
            return -2

    def __normal_form_game(self, other):
        s1 = self.get_age_group()
        s2 = other.get_age_group()
        d1 = self.strength + s1
        d2 = other.strength + s2
        payoffs = {
            (Strategy.cooperate, Strategy.cooperate): (3, 3),
            (Strategy.cooperate, Strategy.defect): (0, 5),
            (Strategy.defect, Strategy.cooperate): (5, 0),
            (Strategy.defect, Strategy.defect): (1 + d1, 1 + d2),
        }

        my_fight_history = []
        for entry in self.fight_history:
            if entry.opponent_pk == other.pk:
                my_fight_history.append(entry)
        their_fight_history = []
        for entry in other.fight_history:
            if entry.opponent_pk == self.pk:
                their_fight_history.append(entry)

        strategy1 = self.personality.get_strategy(None, my_fight_history)
        strategy2 = other.personality.get_strategy(strategy1, their_fight_history)

        self.fight_history.append(FightEntry(self.pk, other.pk, self.simulation.time, strategy1, strategy2))
        other.fight_history.append(FightEntry(other.pk, self.pk, self.simulation.time, strategy2, strategy1))

        return payoffs[(strategy1, strategy2)]

    def get_number_of_people_near(self, distance=5):
        count = 0
        for location in self.memory.people:
            if self.is_near(self.location, location, distance):
                count += 1
        return count

    def is_near(self, location1, location2, distance=5):
        d1 = self.get_distance(location1, location2)
        if d1 < distance:
            return True

    def dont_know_where_anything_is(self):
        if (self.get_on_my_floor(self.memory.doors) or
                self.get_on_my_floor(self.memory.exits) or
                self.get_on_my_floor(self.memory.exit_plans) or
                self.get_on_my_floor(self.memory.stairs)
        ):
            return False
        return True

    def is_good_fighter(self):
        return 17 < self.age < 45 and self.strength > self.simulation.max_strength // 2

    def get_on_my_floor(self, lst):
        new_lst = []
        for location in lst:
            if location[0] == self.location[0]:
                new_lst.append(location)
        return new_lst

    def know_about_important_location(self):
        if self.get_on_my_floor(self.memory.exits) or self.get_on_my_floor(
                self.memory.exit_plans) or self.get_on_my_floor(self.memory.stairs):
            return True
        return False

    def is_in_room(self):
        return self.room_type == "room"

    def is_in_hall(self):
        return self.room_type == "hallway"

    def is_trapped_by_fire(self):
        farthest_empty = self.get_furthest(self.location, self.memory.empties)
        grid_with_blocked = self.get_grid(0)
        path_with_blocked = self.get_path(farthest_empty, grid_with_blocked)
        grid_with_unblocked = self.get_grid(2)
        path_with_unblocked = self.get_path(farthest_empty, grid_with_unblocked)
        return self.__is_trapped(path_with_blocked, path_with_unblocked)

    def is_trapped_by_people(self):
        farthest_empty = self.get_furthest(self.location, self.memory.empties)
        grid_with_blocked = self.get_grid(0)
        path_with_blocked = self.get_path(farthest_empty, grid_with_blocked)
        grid_with_unblocked = self.get_grid(1)
        path_with_unblocked = self.get_path(farthest_empty, grid_with_unblocked)
        return self.__is_trapped(path_with_blocked, path_with_unblocked)

    @staticmethod
    def __is_trapped(path_with_blocked, path_with_unblocked):
        if path_with_blocked:
            return False
        if path_with_unblocked:
            return True
        return False

    def is_trapped(self):
        return self.is_trapped_by_fire() or self.is_trapped_by_people()

    def lots_of_people_near(self):
        return self.get_number_of_people_near() > 5

    def has_good_health(self):
        return self.health > 50

    def has_low_health(self):
        return self.health < 25

    def fire_nearby(self):
        for location in self.memory.fires:
            if self.is_near(self.location, location):
                return True
        return False

    def can_get_to_broken_glass(self):
        closest_broken_glass = self.get_closest(self.location, self.memory.broken_glasses)
        if closest_broken_glass:
            return self.can_get_to_location(closest_broken_glass)
        return False

    def can_get_to_window(self):
        closest_glass = self.get_closest(self.location, self.memory.glasses)
        if closest_glass:
            return self.can_get_to_location(closest_glass)
        return False

    def can_get_to_location(self, location):
        grid = self.get_grid(0)
        path = self.get_path(location, grid)
        if path:
            return True
        return False
