from src.simulation.logger import setup_logger
from src.simulation.colors import colors
from .strategy import Strategy
from .fight_entry import FightEntry
from .thinker import Thinker
from .vision import Vision
from .movement import Movement
from os import mkdir


class Person:

    def __init__(self,
                 simulation,
                 name,
                 pk,
                 location,
                 memory,
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
        mkdir(f'../logs/run{simulation.simulation_count}/people/person{pk}')
        self.logger = setup_logger("person_logger", f'../logs/run{simulation.simulation_count}/people/person{pk}/person{pk}.log', simulation.verbose)
        self.logger.info('This log is for INFO purposes from person')

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
            self.color = colors["follower"]
        else:
            self.color_title = "Light Yellow"
            self.color = colors["nonfollower"]

        self.memory = memory

        self.end_turn_in_fire = True

        self.personality = personality
        self.personality_title = personality_title

        self.fight_history = []

        self.thinker = Thinker(self)

        self.vision = Vision(self)

        self.movement = Movement(self)

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
        self.logger.info(f"{self.name} has won {self.number_of_fights_won} fights.")
        self.logger.info(f"{self.name} has lost {self.number_of_fights_lost} fights.")
        self.logger.info(f"{self.name} has tied {self.number_of_fights_tied} fights.")
        self.logger.info(f"{self.name} has touched fire {self.number_of_fire_touches} times.")
        self.logger.info(f"{self.name} has reached max fear {self.number_of_max_fear} times.")

    def __str__(self):
        return f"{self.name} {self.personality_title} {self.color_title} {self.health} {self.location}."

    def is_dead(self):
        return self.health <= 0

    def place(self, location):
        self.simulation.is_in_building(location)
        if not self.is_one_away(self.location, location):
            raise Exception(f"location is not one away: {location}")
        if not self.simulation.is_valid_location_for_person(location):
            raise Exception(f"location is not valid: {location} {self.simulation.building.text[location[0]][location[1]][location[2]]}")
        other = self.simulation.is_person(location)
        if other is not None:
            return other
        self.location = location
        return None

    @staticmethod
    def is_one_away(location1, location2):
        if location1[0] != location2[0]:
            return False
        a = abs(location1[1] - location2[1])
        b = abs(location1[2] - location2[2])
        if a > 1 or b > 1:
            return False
        return True

    def is_next_to(self, lst):
        for location in lst:
            if self.is_one_away(self.location, location):
                return True
        return False

    def break_glass(self, glass_location):
        if self.is_one_away(self.location, glass_location):
            if self.can_break_glass():
                # the person breaks the glass and hurts themselves doing it
                self.simulation.building.text[glass_location[0]][glass_location[1]][glass_location[2]] = 'b'
                self.memory.add("broken_glasses", glass_location)
                self.health -= 25
            else:
                # too weak to break the glass, but they still hurt themselves trying
                self.health -= 5
            return True
        return False

    def can_break_glass(self):
        return self.strength > 5

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
        d1 = self.movement.get_distance(location1, location2)
        if d1 < distance:
            return True

    def dont_know_where_anything_is(self):
        if (self.get_on_my_floor(self.memory.doors) or
                self.get_on_my_floor(self.memory.exits) or
                self.get_on_my_floor(self.memory.exit_plans) or
                self.get_on_my_floor(self.memory.stairs)):
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
        farthest_empty = self.movement.get_furthest(self.location, self.memory.empties)
        grid_with_blocked = self.movement.get_grid(0)
        path_with_blocked = self.movement.get_path(farthest_empty, grid_with_blocked)
        grid_with_unblocked = self.movement.get_grid(2)
        path_with_unblocked = self.movement.get_path(farthest_empty, grid_with_unblocked)
        return self.__is_trapped(path_with_blocked, path_with_unblocked)

    def is_trapped_by_people(self):
        farthest_empty = self.movement.get_furthest(self.location, self.memory.empties)
        grid_with_blocked = self.movement.get_grid(0)
        path_with_blocked = self.movement.get_path(farthest_empty, grid_with_blocked)
        grid_with_unblocked = self.movement.get_grid(1)
        path_with_unblocked = self.movement.get_path(farthest_empty, grid_with_unblocked)
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
        return self.health <= 50

    def fire_nearby(self):
        for location in self.memory.fires:
            if self.is_near(self.location, location):
                return True
        return False

    def can_get_to_broken_glass(self):
        closest_broken_glass = self.movement.get_closest(self.location, self.memory.broken_glasses)
        if closest_broken_glass:
            return self.can_get_to_location(closest_broken_glass)
        return False

    def can_get_to_window(self):
        closest_glass = self.movement.get_closest(self.location, self.memory.glasses)
        if closest_glass:
            return self.can_get_to_location(closest_glass)
        return False

    def can_get_to_location(self, location):
        grid = self.movement.get_grid(0)
        path = self.movement.get_path(location, grid)
        if path:
            return True
        return False
