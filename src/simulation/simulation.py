from .person.person import Person
from .person.memory import Memory
from .person.personality import Copycat, Cooperator, Detective, Simpleton, Cheater, Grudger, Random, Copykitten
from random import randint
from .building import Building
from .logger import setup_logger
import logging
import inspect


class Simulation:
    def __init__(self,
                 number_of_people=50,
                 simulation_count=0,
                 time_for_firefighters=1000,
                 fire_spread_rate=0.2,
                 max_visibility=5,
                 min_visibility=1,
                 max_strength=10,
                 min_strength=1,
                 max_speed=5,
                 min_speed=1,
                 max_fear=10,
                 min_fear=1,
                 max_age=80,
                 min_age=10,
                 max_health=100,
                 min_health=80,
                 follower_probability=0.5,
                 verbose=False,
                 choice_mode=0,
                 familiarity=15,
                 personalities=None
                 ):
        if personalities is None:
            personalities = {
                "Copycat": 0.125,
                "Cooperator": 0.125,
                "Detective": 0.125,
                "Simpleton": 0.125,
                "Cheater": 0.125,
                "Grudger": 0.125,
                "Copykitten": 0.125,
                "Random": 0.125
            }

        self.logger = setup_logger("simulation_logger", f'../logs/run{simulation_count}/simulation/simulation.log', verbose)
        self.logger.info('This log is for INFO purposes from simulation')

        self.personalities = personalities
        self.max_number_of_copycat = int(personalities["Copycat"] * number_of_people)
        self.number_of_copycat = 0
        self.max_number_of_cooperator = int(personalities["Cooperator"] * number_of_people)
        self.number_of_cooperator = 0
        self.max_number_of_detective = int(personalities["Detective"] * number_of_people)
        self.number_of_detective = 0
        self.max_number_of_simpleton = int(personalities["Simpleton"] * number_of_people)
        self.number_of_simpleton = 0
        self.max_number_of_cheater = int(personalities["Cheater"] * number_of_people)
        self.number_of_cheater = 0
        self.max_number_of_grudger = int(personalities["Grudger"] * number_of_people)
        self.number_of_grudger = 0
        self.max_number_of_copykitten = int(personalities["Copykitten"] * number_of_people)
        self.number_of_copykitten = 0
        self.max_number_of_random = int(personalities["Random"] * number_of_people)
        self.number_of_random = 0

        self.fix_numbers(number_of_people)

        self.max_visibility = max_visibility
        self.min_visibility = min_visibility
        self.max_strength = max_strength
        self.min_strength = min_strength
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.max_fear = max_fear
        self.min_fear = min_fear
        self.max_age = max_age
        self.min_age = min_age
        self.max_health = max_health
        self.min_health = min_health
        self.follower_probability = follower_probability
        self.familiarity = familiarity

        self.number_of_people_that_got_out = 0
        self.number_of_fights = 0
        self.number_of_injuries = 0
        self.number_of_deaths = 0
        self.number_of_deaths_by_fire = 0
        self.number_of_deaths_by_fighting = 0
        self.number_of_deaths_by_moving = 0
        self.number_of_max_fear = 0
        self.number_of_followers = 0
        self.average_fear = 0
        self.average_health = 0
        self.average_age = 0
        self.average_familiarity = 0
        self.average_speed = 0
        self.average_strength = 0
        self.average_visibility = 0

        self.fire_spread_rate = fire_spread_rate
        self.number_of_people = number_of_people
        self.simulation_count = simulation_count
        self.time_for_firefighters = time_for_firefighters
        self.verbose = verbose
        self.choice_mode = choice_mode
        self.live_people = []
        self.dead_people = []
        self.fire_locations = []

        self.time = 0

        self.building = Building(self)
        self.__generate_people()
        self.get_averages()
        self.__start_fire()

        self.logger.info("Simulation has been initialized")
        self.logger.info(f"Number of people: {number_of_people}")
        self.logger.info(f"Time for firefighters: {time_for_firefighters}")
        self.logger.info(f"Fire spread rate: {fire_spread_rate}")
        self.logger.info(f"Max visibility: {max_visibility}")
        self.logger.info(f"Min visibility: {min_visibility}")
        self.logger.info(f"Max strength: {max_strength}")
        self.logger.info(f"Min strength: {min_strength}")
        self.logger.info(f"Max speed: {max_speed}")
        self.logger.info(f"Min speed: {min_speed}")
        self.logger.info(f"Max fear: {max_fear}")
        self.logger.info(f"Min fear: {min_fear}")
        self.logger.info(f"Max age: {max_age}")
        self.logger.info(f"Min age: {min_age}")
        self.logger.info(f"Max health: {max_health}")
        self.logger.info(f"Min health: {min_health}")
        self.logger.info(f"Follower probability: {follower_probability}")
        self.logger.info(f"Familiarity: {familiarity}")
        self.logger.info(f"Number of personalities: {personalities}")
        self.logger.info(f"Number of copycat: {self.max_number_of_copycat}")
        self.logger.info(f"Number of cooperator: {self.max_number_of_cooperator}")
        self.logger.info(f"Number of detective: {self.max_number_of_detective}")
        self.logger.info(f"Number of simpleton: {self.max_number_of_simpleton}")
        self.logger.info(f"Number of cheater: {self.max_number_of_cheater}")
        self.logger.info(f"Number of grudger: {self.max_number_of_grudger}")
        self.logger.info(f"Number of copykitten: {self.max_number_of_copykitten}")
        self.logger.info(f"Number of random: {self.max_number_of_random}")

    def fix_numbers(self, number_of_people):
        current_number = self.max_number_of_copycat + self.max_number_of_cooperator + self.max_number_of_detective + self.max_number_of_simpleton + self.max_number_of_cheater + self.max_number_of_grudger + self.max_number_of_copykitten + self.max_number_of_random
        maxes = [self.max_number_of_copycat, self.max_number_of_cooperator, self.max_number_of_detective,
                 self.max_number_of_simpleton, self.max_number_of_cheater, self.max_number_of_grudger,
                 self.max_number_of_copykitten, self.max_number_of_random]
        if current_number < number_of_people:
            max_ = -1
            for m in maxes:
                if m > max_:
                    max_ = m
            max_index = maxes.index(max_)
            maxes[max_index] += number_of_people - current_number
        elif current_number > number_of_people:
            max_ = -1
            for m in maxes:
                if m > max_:
                    max_ = m
            max_index = maxes.index(max_)
            maxes[max_index] -= current_number
        self.max_number_of_copycat = maxes[0]
        self.max_number_of_cooperator = maxes[1]
        self.max_number_of_detective = maxes[2]
        self.max_number_of_simpleton = maxes[3]
        self.max_number_of_cheater = maxes[4]
        self.max_number_of_grudger = maxes[5]
        self.max_number_of_copykitten = maxes[6]
        self.max_number_of_random = maxes[7]

    def get_averages(self):
        for person in self.live_people:
            self.average_fear += person.fear
            self.average_health += person.health
            self.average_age += person.age
            self.average_familiarity += person.familiarity
            self.average_speed += person.speed
            self.average_strength += person.strength
            self.average_visibility += person.visibility
        if len(self.live_people) > 0:
            self.average_fear /= len(self.live_people)
            self.average_health /= len(self.live_people)
            self.average_age /= len(self.live_people)
            self.average_familiarity /= len(self.live_people)
            self.average_speed /= len(self.live_people)
            self.average_strength /= len(self.live_people)
            self.average_visibility /= len(self.live_people)

    def __start_fire(self):
        while True:
            floor = randint(0, len(self.building.text) - 1)
            x = randint(0, len(self.building.text[0]) - 1)
            y = randint(0, len(self.building.text[0][0]) - 1)
            location = (floor, x, y)
            if self.__set_fire(location):
                break

    def __generate_people(self):
        pk = 0
        while pk < self.number_of_people:
            floor = randint(0, len(self.building.text) - 1)
            location = (floor, randint(0, len(self.building.text[0]) - 1),
                        randint(0, len(self.building.text[0][0]) - 1))
            if (self.is_mini_obstacle(location) or self.is_normal_obstacle(location) or self.is_large_obstacle(location) or self.is_fire(location) or self.is_person(location) or
                    self.is_wall(location) or self.is_stair(location) or self.is_glass(location) or
                    self.is_door(location) or self.is_exit(location)):
                continue
            self.generate_person(location, pk)
            pk += 1

    def generate_person(self, location, pk):
        familiarity, memory = self.generate_starting_memory()
        personality, personality_title = self.get_personality()
        if personality is None:
            raise Exception("Personality is None")
        age = randint(self.min_age, self.max_age)
        health = randint(self.min_health, self.max_health)
        speed = randint(self.min_speed, self.max_speed)
        strength = randint(self.min_strength, self.max_strength)
        visibility = randint(self.min_visibility, self.max_visibility)
        fear = randint(self.min_fear, self.max_fear)
        is_follower = randint(0, 1) < self.follower_probability
        person = Person(self,
                        f'Person{pk}',
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
                        )
        self.number_of_followers += 1 if is_follower else 0
        self.live_people.append(person)
        self.logger.info(f"Person{pk} has been generated at location {location}")

    def generate_starting_memory(self):
        object_list = ['doors', 'exits', 'stairs']
        memory = Memory()
        familiarity = randint(0, self.familiarity)
        for _ in range(0, familiarity):
            what = object_list[randint(0, len(object_list) - 1)]
            where = self.building.object_locations[what][randint(0, len(self.building.object_locations[what]) - 1)]
            memory.add(what, where)
        return familiarity, memory

    def get_personality(self):
        if self.number_of_copycat < self.max_number_of_copycat:
            self.number_of_copycat += 1
            return Copycat(), "Copycat"
        if self.number_of_cooperator < self.max_number_of_cooperator:
            self.number_of_cooperator += 1
            return Cooperator(), "Cooperator"
        if self.number_of_detective < self.max_number_of_detective:
            self.number_of_detective += 1
            return Detective(), "Detective"
        if self.number_of_simpleton < self.max_number_of_simpleton:
            self.number_of_simpleton += 1
            return Simpleton(), "Simpleton"
        if self.number_of_cheater < self.max_number_of_cheater:
            self.number_of_cheater += 1
            return Cheater(), "Cheater"
        if self.number_of_grudger < self.max_number_of_grudger:
            self.number_of_grudger += 1
            return Grudger(), "Grudger"
        if self.number_of_copykitten < self.max_number_of_copykitten:
            self.number_of_copykitten += 1
            return Copykitten(), "Copykitten"
        if self.number_of_random < self.max_number_of_random:
            self.number_of_random += 1
            return Random(), "Random"
        return None

    def statistics(self):
        self.get_averages()
        self.logger.info(f"Number of people: {self.number_of_people}")
        self.logger.info(f"Number of dead people: {len(self.dead_people)}")
        self.logger.info(f"Number of live people: {len(self.live_people)}")
        self.logger.info(f"Number of fire locations: {len(self.fire_locations)}")
        self.logger.info(f"Number of people that got out: {self.number_of_people_that_got_out}")
        self.logger.info(f"Number of fights: {self.number_of_fights}")
        self.logger.info(f"Number of injuries: {self.number_of_injuries}")
        self.logger.info(f"Number of deaths: {self.number_of_deaths}")
        self.logger.info(f"Number of deaths by fire: {self.number_of_deaths_by_fire}")
        self.logger.info(f"Number of deaths by fighting: {self.number_of_deaths_by_fighting}")
        self.logger.info(f"Number of deaths by moving: {self.number_of_deaths_by_moving}")
        self.logger.info(f"Number of max fear: {self.number_of_max_fear}")
        self.logger.info(f"Number of followers: {self.number_of_followers}")
        self.logger.info(f"Average fear: {self.average_fear}")
        self.logger.info(f"Average health: {self.average_health}")
        self.logger.info(f"Average age: {self.average_age}")
        self.logger.info(f"Average familiarity: {self.average_familiarity}")
        self.logger.info(f"Average speed: {self.average_speed}")
        self.logger.info(f"Average strength: {self.average_strength}")
        self.logger.info(f"Average visibility: {self.average_visibility}")

    def evacuate(self):
        self.logger.info("Evacuating...")
        while len(self.live_people) > 0 and self.time < self.time_for_firefighters:
            self.time += 1
            self.logger.info(f"Time: {self.time}")
            self.building.refresh()
            self.building.print()
            self.__move_people()
            self.logger.info("People have moved")
            self.__spread_fire()
            self.logger.info("Fire has spread")
            self.statistics()
        self.logger.info("Evacuation complete")

    def __move_people(self):
        logging.info("Moving people")
        temp_live_people = []
        for person in self.live_people:
            logging.info(f"{person.name} is moving")
            # Die by fighting someone else during their turn
            if self.__is_dead(person):
                self.logger.info(f"{person.name} has died during their turn")
                continue

            if person.end_turn_in_fire and person.location in self.fire_locations:
                self.number_of_injuries += 1
                person.health -= 50
            elif not person.end_turn_in_fire and person.location in self.fire_locations:
                self.number_of_injuries += 1
                person.health -= 25

            # Die by fire
            if self.__is_dead(person):
                self.logger.info(f"{person.name} has died by fire")
                self.number_of_deaths_by_fire += 1
                continue

            other_person = person.movement.run()

            # Die by moving
            if self.__is_dead(person):
                self.logger.info(f"{person.name} has died by moving")
                self.number_of_deaths_by_moving += 1
                continue

            if other_person:
                self.logger.info(f"{person.name} is fighting {other_person.name}")
                person.combat(other_person)
                self.number_of_fights += 1
                self.number_of_injuries += 2

            # Die by combat
            if self.__is_dead(person):
                self.logger.info(f"{person.name} has died by combat")
                self.number_of_deaths_by_fighting += 1
                continue

            # the person is still alive and made it to an exit
            if self.is_exit(person.location):
                self.number_of_people_that_got_out += 1
                self.logger.info(f"{person.name} has escaped by exiting")
                continue

            if self.is_broken_glass(person.location):
                self.get_hurt_from_jumping_out_of_window(person)
                if self.__is_dead(person):
                    self.logger.info(f"{person.name} has died by broken glass")
                    continue
                self.number_of_people_that_got_out += 1
                self.logger.info(f"{person.name} has escaped by jumping out of window")
                continue
            self.number_of_max_fear += 1 if person.fear == self.max_fear else 0
            temp_live_people.append(person)
            self.logger.info(f"{person.name} has moved to location {person.location}")

        self.live_people = temp_live_people

    @staticmethod
    def get_hurt_from_jumping_out_of_window(person):
        floor = person.location[0]
        # hurt self on broken glass
        person.health -= randint(0, 10)
        if floor == 2:
            # hurt self on the way down
            person.health -= randint(10, 30)
        elif floor == 3:
            # hurt self on the way down
            person.health -= randint(30, 50)
        elif floor > 3:
            # hurt self on the way down
            person.health -= randint(50, 100)

    def __is_dead(self, person):
        if person.is_dead():
            self.number_of_deaths += 1
            self.dead_people.append(person)
            if self.verbose:
                print(f"{person.name} has died at location {person.location}")
            return True
        return False

    def __spread_fire(self):
        for fire_location in self.fire_locations:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if self.__is_fire_spread():
                        new_location = (fire_location[0], fire_location[1] + i, fire_location[2] + j)
                        self.__set_fire(new_location)

    def __set_fire(self, location):
        self.is_in_building(location)
        if not self.is_fire(location):
            # remove what was there
            self.building.text[location[0]][location[1]][location[2]] = 'f'
            self.fire_locations.append(location)
            self.logger.info(f"Fire has started at location {location}")
            return True
        return False

    def __is_fire_spread(self):
        chance = int(self.fire_spread_rate * 100)
        return randint(0, 100) < chance

    def is_exit(self, location):
        self.is_in_building(location)
        return self.building.text[location[0]][location[1]][location[2]] == 'e'

    def is_mini_obstacle(self, location):
        self.is_in_building(location)
        c = self.building.text[location[0]][location[1]][location[2]]
        return c == 'm'

    def is_normal_obstacle(self, location):
        self.is_in_building(location)
        c = self.building.text[location[0]][location[1]][location[2]]
        return c == 'n'

    def is_large_obstacle(self, location):
        self.is_in_building(location)
        c = self.building.text[location[0]][location[1]][location[2]]
        return c == 'l'

    def is_fire(self, location):
        self.is_in_building(location)
        return location in self.fire_locations

    def is_person(self, location):
        for person in self.live_people:
            if person.location == location:
                return person
        return None

    def is_wall(self, location):
        self.is_in_building(location)
        c = self.building.text[location[0]][location[1]][location[2]]
        return c == 'w' or c == 'h'

    def is_half_wall(self, location):
        self.is_in_building(location)
        c = self.building.text[location[0]][location[1]][location[2]]
        return c == 'h'

    def is_in_building(self, location):
        if 0 <= location[0] < self.building.floor_size and 0 <= location[1] < self.building.x_size and 0 <= location[2] < self.building.y_size:
            return True
        raise Exception(f"Location is not in building: {location} Caller name: {inspect.currentframe().f_back.f_code.co_name}")

    def is_stair(self, location):
        self.is_in_building(location)
        return self.building.text[location[0]][location[1]][location[2]] == 's'

    def is_glass(self, location):
        self.is_in_building(location)
        return self.building.text[location[0]][location[1]][location[2]] == 'g'

    def is_empty(self, location):
        self.is_in_building(location)
        return self.building.text[location[0]][location[1]][location[2]] == ' '

    def is_door(self, location):
        self.is_in_building(location)
        return self.building.text[location[0]][location[1]][location[2]] == 'd'

    def is_broken_glass(self, location):
        self.is_in_building(location)
        return self.building.text[location[0]][location[1]][location[2]] == 'b'

    def is_room(self, location):
        self.is_in_building(location)
        return self.building.text[location[0]][location[1]][location[2]] == '1'

    def is_hallway(self, location):
        self.is_in_building(location)
        return self.building.text[location[0]][location[1]][location[2]] == '2'

    def is_exit_plan(self, location):
        self.is_in_building(location)
        return self.building.text[location[0]][location[1]][location[2]] == 'p'

    def is_valid_location_for_person(self, location):
        return not self.is_large_obstacle(location) and not self.is_wall(location) and not self.is_glass(location)
