from person import Person
from memory import Memory
from random import randint
from building import Building
import logging


class Simulation:
    def __init__(self, number_of_people, n, time_for_firefights, verbose=False, with_ai=False):
        logging.basicConfig(filename=f'../logs/run{n}/simulation.log', level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
        self.number_of_people_that_got_out = 0
        self.number_of_people = number_of_people
        self.n = n
        self.time_for_firefights = time_for_firefights
        self.verbose = verbose
        self.with_ai = with_ai
        self.live_people = []
        self.dead_people = []
        self.fire_locations = []
        self.building = Building(self)
        self.__generate_people()
        self.__start_fire()

    def __start_fire(self):
        while True:
            floor = randint(0, len(self.building.text_building)-1)
            x = randint(0, len(self.building.text_building[0])-1)
            y = randint(0, len(self.building.text_building[0][0])-1)
            location = (floor, x, y)
            if self.__set_fire(location):
                break

    def __generate_people(self):
        object_list = ['doors', 'exits', 'stairs']
        count = 0
        while count < self.number_of_people:
            floor = randint(0, len(self.building.text_building)-1)
            location = (floor, randint(0, len(self.building.text_building[0])-1), randint(0, len(self.building.text_building[0][0])-1))
            if (self.is_obstacle(location) or self.is_fire(location) or self.is_person(location) or
                    self.is_wall(location) or self.is_stair(location) or self.is_glass(location) or
                    self.is_door(location) or self.is_exit(location)):
                continue
            memory = Memory()
            familiarity = randint(0, 10)
            for _ in range(0, familiarity):
                what = object_list[randint(0, len(object_list)-1)]
                where = self.building.object_locations[what][randint(0, len(self.building.object_locations[what])-1)]
                memory.add(what, where)
            self.live_people.append(Person(self, f'Person{count}', count, location, memory, self.n, self.verbose))
            logging.info(f"Person{count} has been generated at location {location}")
            count += 1

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
        time = 0
        while len(self.live_people) > 0 and time < self.time_for_firefights:
            logging.info(f"Anew turn has started-------")
            self.building.refresh()
            if self.verbose:
                self.building.print_building()
                print(f"{self.number_of_people} people remaining")
            logging.info(f"{self.number_of_people} people remaining")
            self.__move_people()
            self.__spread_fire()
            time += 1
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
                person.health -= 50
            elif not person.end_turn_in_fire and person.location in self.fire_locations:
                person.health -= 25

            # Die by fire
            if self.__is_dead(person):
                logging.info(f"{person.name} has died by fire")
                continue

            other_person = person.move()

            # Die by moving
            if self.__is_dead(person):
                logging.info(f"{person.name} has died by moving")
                continue

            if other_person:
                logging.info(f"{person.name} is fighting {other_person.name}")
                person.combat(other_person)

            # Die by combat
            if self.__is_dead(person):
                logging.info(f"{person.name} has died by combat")
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

            temp_live_people.append(person)

        self.live_people = temp_live_people

    def __is_dead(self, person):
        if person.is_dead():
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
        if not self.is_fire(location):
            # remove what was there
            self.building.text_building[location[0]][location[1]][location[2]] = 'f'
            self.fire_locations.append(location)
            return True
        return False

    @staticmethod
    def __is_fire_spread():
        return randint(0, 20) == 1

    def is_exit(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == 'e'

    def is_obstacle(self, location):
        c = self.building.text_building[location[0]][location[1]][location[2]]
        return c == 'm' or c == 'n' or c == 'l'

    def is_fire(self, location):
        return location in self.fire_locations

    def is_person(self, location):
        for person in self.live_people:
            if person.location == location:
                return person
        return None

    def is_wall(self, location):
        c = self.building.text_building[location[0]][location[1]][location[2]]
        return c == 'w' or c == 'h'

    def is_in_building(self, location):
        return 0 <= location[0] < len(self.building.text_building) and 0 <= location[1] < len(self.building.text_building[0]) and 0 <= location[2] < len(self.building.text_building[0][0])

    def is_stair(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == 's'

    def is_glass(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == 'g'

    def is_empty(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == ' '

    def is_door(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == 'd'

    def is_broken_glass(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == 'b'

    def is_room(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == '1'

    def is_hallway(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == '2'

    def is_exit_plan(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == 'p'
