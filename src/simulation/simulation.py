from simulation.person.person import Person
from simulation.person.memory import Memory
from simulation.person.personality import Copycat, Cooperator, Detective, Simpleton, Cheater, Grudger, Random, Copykitten
from random import randint
from .building import Building
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
        logging.basicConfig(filename=f'../../logs/run{simulation_count}/simulation.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

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
            floor = randint(0, len(self.building.text_building) - 1)
            x = randint(0, len(self.building.text_building[0]) - 1)
            y = randint(0, len(self.building.text_building[0][0]) - 1)
            location = (floor, x, y)
            if self.__set_fire(location):
                break

    def __generate_people(self):
        object_list = ['doors', 'exits', 'stairs']
        count = 0
        while count < self.number_of_people:
            floor = randint(0, len(self.building.text_building) - 1)
            location = (floor, randint(0, len(self.building.text_building[0]) - 1),
                        randint(0, len(self.building.text_building[0][0]) - 1))
            if (self.is_obstacle(location) or self.is_fire(location) or self.is_person(location) or
                    self.is_wall(location) or self.is_stair(location) or self.is_glass(location) or
                    self.is_door(location) or self.is_exit(location)):
                continue
            memory = Memory()
            familiarity = randint(0, self.familiarity)
            for _ in range(0, familiarity):
                what = object_list[randint(0, len(object_list) - 1)]
                where = self.building.object_locations[what][randint(0, len(self.building.object_locations[what]) - 1)]
                memory.add(what, where)
            personality = self.get_personality()
            if personality is None:
                raise Exception("Personality is None")
            person = Person(self,
                            f'Person{count}',
                            count,
                            location,
                            memory,
                            self.simulation_count,
                            self.verbose,
                            self.max_visibility,
                            self.min_visibility,
                            self.max_strength,
                            self.min_strength,
                            self.max_speed,
                            self.min_speed,
                            self.max_fear,
                            self.min_fear,
                            self.max_age,
                            self.min_age,
                            self.max_health,
                            self.min_health,
                            self.follower_probability,
                            familiarity,
                            personality
                            )
            self.number_of_followers += 1 if person.is_follower else 0
            self.live_people.append(person)
            logging.info(f"Person{count} has been generated at location {location}")
            count += 1

    def get_personality(self):
        if self.number_of_copycat < self.max_number_of_copycat:
            self.number_of_copycat += 1
            return Copycat()
        if self.number_of_cooperator < self.max_number_of_cooperator:
            self.number_of_cooperator += 1
            return Cooperator()
        if self.number_of_detective < self.max_number_of_detective:
            self.number_of_detective += 1
            return Detective()
        if self.number_of_simpleton < self.max_number_of_simpleton:
            self.number_of_simpleton += 1
            return Simpleton()
        if self.number_of_cheater < self.max_number_of_cheater:
            self.number_of_cheater += 1
            return Cheater()
        if self.number_of_grudger < self.max_number_of_grudger:
            self.number_of_grudger += 1
            return Grudger()
        if self.number_of_copykitten < self.max_number_of_copykitten:
            self.number_of_copykitten += 1
            return Copykitten()
        if self.number_of_random < self.max_number_of_random:
            self.number_of_random += 1
            return Random()
        return None

    def statistics(self):
        if self.verbose:
            print(f"Number of people: {self.number_of_people}")
            print(f"Number of dead people: {len(self.dead_people)}")
            print(f"Number of live people: {len(self.live_people)}")
            print(f"Number of fire locations: {len(self.fire_locations)}")
        logging.info(f"Number of people: {self.number_of_people}")
        logging.info(f"Number of dead people: {len(self.dead_people)}")
        logging.info(f"Number of live people: {len(self.live_people)}")
        logging.info(f"Number of fire locations: {len(self.fire_locations)}")

    def evacuate(self):
        if self.verbose:
            print("Evacuating...")
        logging.info("Evacuating...")
        while len(self.live_people) > 0 and self.time < self.time_for_firefighters:
            self.time += 1
            logging.info(f"Anew turn has started-------")
            self.building.refresh()
            if self.verbose:
                self.building.print_building()
                print(f"{self.number_of_people} people remaining")
            logging.info(f"{self.number_of_people} people remaining")
            self.__move_people()
            self.__spread_fire()
        if self.verbose:
            print("Evacuation complete")
        logging.info("Evacuation complete")

    def __move_people(self):
        logging.info("Moving people")
        temp_live_people = []
        for person in self.live_people:
            logging.info(f"{person.name} is moving")
            # Die by fighting someone else during their turn
            if self.__is_dead(person):
                logging.info(f"{person.name} has died during their turn")
                continue

            if person.end_turn_in_fire and person.location in self.fire_locations:
                self.number_of_injuries += 1
                person.health -= 50
            elif not person.end_turn_in_fire and person.location in self.fire_locations:
                self.number_of_injuries += 1
                person.health -= 25

            # Die by fire
            if self.__is_dead(person):
                logging.info(f"{person.name} has died by fire")
                self.number_of_deaths_by_fire += 1
                continue

            other_person = person.move()

            # Die by moving
            if self.__is_dead(person):
                logging.info(f"{person.name} has died by moving")
                self.number_of_deaths_by_moving += 1
                continue

            if other_person:
                logging.info(f"{person.name} is fighting {other_person.name}")
                person.combat(other_person)
                self.number_of_fights += 1
                self.number_of_injuries += 2

            # Die by combat
            if self.__is_dead(person):
                logging.info(f"{person.name} has died by combat")
                self.number_of_deaths_by_fighting += 1
                continue

            # the person is still alive and made it to an exit
            if self.is_exit(person.location):
                self.number_of_people_that_got_out += 1
                logging.info(f"{person.name} has escaped by exiting")
                if self.verbose:
                    print(f"{person.name} has escaped by exiting")
                continue

            if self.is_broken_glass(person.location):
                self.number_of_people_that_got_out += 1
                logging.info(f"{person.name} has escaped by jumping out of window")
                if self.verbose:
                    print(f"{person.name} has escaped by jumping out of window")
                continue
            self.number_of_max_fear += 1 if person.fear == self.max_fear else 0
            temp_live_people.append(person)

        self.live_people = temp_live_people

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
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        if not self.is_fire(location):
            # remove what was there
            self.building.text_building[location[0]][location[1]][location[2]] = 'f'
            self.fire_locations.append(location)
            return True
        return False

    def __is_fire_spread(self):
        chance = int(self.fire_spread_rate * 100)
        return randint(0, 100) < chance

    def is_exit(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        return self.building.text_building[location[0]][location[1]][location[2]] == 'e'

    def is_obstacle(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        c = self.building.text_building[location[0]][location[1]][location[2]]
        return c == 'm' or c == 'n' or c == 'l'

    def is_mini_obstacle(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        c = self.building.text_building[location[0]][location[1]][location[2]]
        return c == 'm'

    def is_normal_obstacle(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        c = self.building.text_building[location[0]][location[1]][location[2]]
        return c == 'n'

    def is_large_obstacle(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        c = self.building.text_building[location[0]][location[1]][location[2]]
        return c == 'l'

    def is_fire(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        return location in self.fire_locations

    def is_person(self, location):
        for person in self.live_people:
            if person.location == location:
                return person
        return None

    def is_wall(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        c = self.building.text_building[location[0]][location[1]][location[2]]
        return c == 'w'

    def is_half_wall(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        c = self.building.text_building[location[0]][location[1]][location[2]]
        return c == 'h'

    def is_in_building(self, location):
        return 0 <= location[0] < len(self.building.text_building) and 0 <= location[1] < len(
            self.building.text_building[0]) and 0 <= location[2] < len(self.building.text_building[0][0])

    def is_stair(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        return self.building.text_building[location[0]][location[1]][location[2]] == 's'

    def is_glass(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        return self.building.text_building[location[0]][location[1]][location[2]] == 'g'

    def is_empty(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        return self.building.text_building[location[0]][location[1]][location[2]] == ' '

    def is_door(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        return self.building.text_building[location[0]][location[1]][location[2]] == 'd'

    def is_broken_glass(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        return self.building.text_building[location[0]][location[1]][location[2]] == 'b'

    def is_room(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        return self.building.text_building[location[0]][location[1]][location[2]] == '1'

    def is_hallway(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        return self.building.text_building[location[0]][location[1]][location[2]] == '2'

    def is_exit_plan(self, location):
        if not self.is_in_building(location):
            raise Exception(f"Location is not in building: {location} \ncaller name: {inspect.currentframe().f_back.f_code.co_name}")
        return self.building.text_building[location[0]][location[1]][location[2]] == 'p'

    def is_valid_location_for_person(self, location):
        return not self.is_large_obstacle(location) and not self.is_wall(location) and not self.is_glass(location)
