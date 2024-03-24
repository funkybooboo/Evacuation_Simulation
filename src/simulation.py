from person import Person
from random import randint


class Simulation:
    def __init__(self, number_of_people, verbose, building):
        self.original_number_of_people = number_of_people
        self.number_of_people = number_of_people
        self.verbose = verbose
        self.building = building
        self.live_people = []
        self.__generate_people()
        self.dead_people = []
        self.fire_locations = [(randint(0, len(self.building.text_building[0])), randint(0, len(self.building.text_building[0][0])))]

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
            memory = {
                "door": [],
                "exit": [],
                "stair": [],
                "glass": [],
                "obstacle": [],
            }
            familiarity = randint(1, 11)
            for _ in range(1, familiarity):
                j = randint(0, len(self.building.object_locations))
                memory[object_list[j]].append(randint(0, len(self.building.object_locations[object_list[j]])))
            self.live_people.append(Person(f'Person{i}', i, location, memory))

    def print_building(self):
        for floor in self.building.color_building.keys():
            for row in range(self.building.color_building[floor]):
                for col in range(self.building.color_building[floor][row]):
                    person = self.__is_person((floor, row, col))
                    if person:
                        print(person.color)
                    else:
                        print(self.building.color_building[floor][row][col])

    def statistics(self):
        if self.verbose:
            print(f"Number of people: {self.number_of_people}")
            print(f"Number of dead people: {len(self.dead_people)}")
            print(f"Number of live people: {len(self.live_people)}")
            print(f"Number of fire locations: {len(self.fire_locations)}")

    def evacuate(self):
        if self.verbose:
            print("Evacuating...")
        while self.number_of_people > 0:
            self.__move_people()
            if self.verbose:
                print(f"{self.number_of_people} people remaining")
            self.__spread_fire()
            self.print_building()
        if self.verbose:
            print("Evacuation complete")

    def __move_people(self):
        for person in self.live_people:
            if self.check_for_dead(person):
                continue
            move_data = self.move(person)
            if move_data:
                if move_data['is_hit']:
                    person1 = self.live_people[move_data['pk1']]
                    person2 = self.live_people[move_data['pk2']]
                    if self.verbose:
                        print(f"{person1.name} and {person2.name} have collided")
                    self.__compete(person1, person2)
                if move_data['is_exit']:
                    self.number_of_people -= 1
                    self.live_people.remove(person)
                    if self.verbose:
                        print(f"{person.name} has exited the building")
            else:
                raise Exception("No move data")

    def check_for_dead(self, person):
        is_dead = False
        for fire_location in self.fire_locations:
            if person.location == fire_location:
                is_dead = True
                if self.verbose:
                    print(f"{person.name} has been caught in the fire at {person.location}")
                self.number_of_people -= 1
                self.dead_people.append(person)
                self.live_people.remove(person)
        return is_dead

    def __spread_fire(self):
        for fire_location in self.fire_locations:
            if self.__is_fire_spread():
                self.fire_locations.append((fire_location[0], fire_location[1] + 1))
            if self.__is_fire_spread():
                self.fire_locations.append((fire_location[0], fire_location[1] - 1))
            if self.__is_fire_spread():
                self.fire_locations.append((fire_location[0] + 1, fire_location[1]))
            if self.__is_fire_spread():
                self.fire_locations.append((fire_location[0] - 1, fire_location[1]))

    @staticmethod
    def __is_fire_spread():
        return randint(0, 20) == 1

    def __compete(self, person1, person2):
        payoffs = self.get_normal_form_game(person1, person2)
        if payoffs[0] > payoffs[1]:
            person2.health -= 1
            # TODO move person1 into the spot
        elif payoffs[0] < payoffs[1]:
            person1.health -= 1
            # TODO move person2 into the spot
        else:
            person1.health -= 1
            person2.health -= 1
            # TODO move no one into the spot

    @staticmethod
    def get_normal_form_game(person1, person2):
        # TODO adjust the payoffs based on the persons strength levels
        base_payoffs = {
            ("cooperate", "cooperate"): (3, 3),
            ("cooperate", "defect"): (0, 5),
            ("defect", "cooperate"): (5, 0),
            ("defect", "defect"): (1, 1),
        }
        return base_payoffs[(person1.strategy, person2.strategy)]

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

    def move(self, person):
        # TODO write a function to move a person return a dictionary with the following keys and values (is_hit, is_exit, pk1, pk2)
        pass
