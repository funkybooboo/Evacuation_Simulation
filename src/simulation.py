from person import Person
from memory import Memory
from random import randint
from building import Building


class Simulation:
    def __init__(self, number_of_people, verbose, with_ai):
        self.number_of_people_that_got_out = 0
        self.number_of_people = number_of_people
        self.verbose = verbose
        self.with_ai = with_ai
        self.building = Building(self)
        self.live_people = []
        self.dead_people = []
        self.__generate_people()
        self.fire_locations = []
        self.__start_fire()

    def __start_fire(self):
        while True:
            floor = randint(0, len(self.building.text_building))
            x = randint(0, len(self.building.text_building[0]))
            y = randint(0, len(self.building.text_building[0][0]))
            location = (floor, x, y)
            if self.__set_fire(location):
                break

    def __generate_people(self):
        object_list = list(self.building.object_locations.keys())
        for i in range(self.number_of_people):
            floor = randint(0, len(self.building.text_building))
            location = (floor, randint(0, len(self.building.text_building[0])), randint(0, len(self.building.text_building[0][0])))
            if (self.__is_obstacle(location) or self.__is_fire(location) or self.__is_person(location) or
                    self.__is_wall(location) or self.__is_stair(location) or self.__is_glass(location) or
                    self.__is_door(location) or self.__is_exit(location)):
                i -= 1
                continue
            memory = Memory()
            familiarity = randint(1, 11)
            for _ in range(1, familiarity):
                what = object_list[randint(0, len(self.building.object_locations))]
                where = object_list[what][randint(0, len(self.building.object_locations[what]))]
                memory.add(what, where)
            self.live_people.append(Person(self, f'Person{i}', i, location, memory, self.verbose))

    def statistics(self):
        if self.verbose:
            print(f"Number of people: {self.number_of_people}")
            print(f"Number of dead people: {len(self.dead_people)}")
            print(f"Number of live people: {len(self.live_people)}")
            print(f"Number of fire locations: {len(self.fire_locations)}")

    def evacuate(self):
        if self.verbose:
            print("Evacuating...")

        while len(self.live_people) > 0:
            self.__move_people()

            self.__spread_fire()

            self.building.print_building()

            if self.verbose:
                print(f"{self.number_of_people} people remaining")

        if self.verbose:
            print("Evacuation complete")

    def __move_people(self):
        temp_live_people = []
        for person in self.live_people:

            # Die by fighting someone else during their turn
            if self.__is_dead(person):
                continue

            if person.end_turn_in_fire and person.location in self.fire_locations:
                person.health -= 50
            elif not person.end_turn_in_fire and person.location in self.fire_locations:
                person.health -= 25

            # Die by fire
            if self.__is_dead(person):
                continue

            other_person = person.move()

            # Die by moving
            if self.__is_dead(person):
                continue

            if other_person is not None:
                person.combat(other_person)

            # Die by combat
            if self.__is_dead(person):
                continue

            # the person is still alive and made it to an exit
            if self.__is_exit(person.location):
                self.number_of_people_that_got_out += 1
                if self.verbose:
                    print(f"{person.name} has escaped by exiting")
                continue

            if self.__is_broken_glass(person.location):
                self.number_of_people_that_got_out += 1
                if self.verbose:
                    print(f"{person.name} has escaped by jumping out of window")
                continue

            temp_live_people.append(person)

        self.live_people = temp_live_people.copy()

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
        if self.__is_location_in_building(location) and not self.__is_fire(location):
            # remove what was there
            self.building.text_building[location[0]][location[1]][location[2]] = 'f'
            self.fire_locations.append(location)
            return True
        return False

    def __is_location_in_building(self, location):
        return 0 <= location[0] < len(self.building.text_building) and 0 <= location[1] < len(self.building.text_building[0]) and 0 <= location[2] < len(self.building.text_building[0][0])

    @staticmethod
    def __is_fire_spread():
        return randint(0, 20) == 1

    def __is_exit(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == 'e'

    def __is_obstacle(self, location):
        c = self.building.text_building[location[0]][location[1]][location[2]]
        return c == 'm' or c == 'n' or c == 'l'

    def __is_fire(self, location):
        return location in self.fire_locations

    def __is_person(self, location):
        for person in self.live_people:
            if person.location == location:
                return person
        return None

    def __is_wall(self, location):
        c = self.building.text_building[location[0]][location[1]][location[2]]
        return c == 'w' or c == 'h'

    def __is_stair(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == 's'

    def __is_glass(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == 'g'

    def __is_empty(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == ' '

    def __is_door(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == 'd'

    def __is_broken_glass(self, location):
        return self.building.text_building[location[0]][location[1]][location[2]] == 'b'

