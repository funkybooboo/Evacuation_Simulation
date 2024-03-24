from person import Person
from random import randint


class Simulation:
    def __init__(self, number_of_people, verbose, building):
        self.number_of_people = number_of_people
        self.verbose = verbose
        self.building = building
        self.live_people = self.__generate_people()
        self.dead_people = []
        self.fire_locations = [(randint(0, len(self.building['floor1']) - 1), randint(0, len(self.building['floor1'][0]) - 1))]

    def __generate_people(self):
        people = []
        people_locations = []
        for i in range(self.number_of_people):
            location = (randint(0, len(self.building['floor1']) - 1), randint(0, len(self.building['floor1'][0]) - 1))
            if location in people_locations || self.__is_obstacle(location) || self.__is_fire(location) || self.__is_person(location) || self.__is_wall(location) || self.__is_stair(location) || self.__is_glass(location) || self.__is_door(location) || self.__is_exit(location):
                i -= 1
                continue
            people_locations.append(location)

            people.append(Person(f'Person{i}', i, location, ))
        return people

    def print_building(self):
        for floor in self.building:
            for row in floor:
                for cell in row:
                    is_person = False
                    for person in self.live_people:
                        if person.location == (row, cell):
                            is_person = True
                            print(person.name, end=" ")
                            break
                    if not is_person:
                        print(cell, end=" ")
                print()
            print()

    def statistics(self):
        if self.verbose:
            self.print_building()
            print(f"Number of people: {self.number_of_people}")

    def evacuate(self):
        if self.verbose:
            print("Evacuating...")
        while self.number_of_people > 0:
            self.__move_people()
            if self.verbose:
                print(f"{self.number_of_people} people remaining")
            self.__spread_fire()
        if self.verbose:
            print("Evacuation complete")

    def __move_people(self):
        for person in self.live_people:
            self.check_for_dead(person)

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
        for fire_location in self.fire_locations:
            if person.location == fire_location:
                if self.verbose:
                    print(f"{person.name} has been caught in the fire")
                self.number_of_people -= 1
                self.dead_people.append(person)
                self.live_people.remove(person)

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

    def get_normal_form_game(self, person1, person2):
        base_payoffs = {
            ("cooperate", "cooperate"): (3, 3),
            ("cooperate", "defect"): (0, 5),
            ("defect", "cooperate"): (5, 0),
            ("defect", "defect"): (1, 1),
        }
        return base_payoffs[(person1.strategy, person2.strategy)]

    def __is_exit(self, location):
        return self.building['floor1'][location[0]][location[1]] == 'e'

    def __is_obstacle(self, location):
        return self.building['floor1'][location[0]][location[1]] == 'o'

    def __is_fire(self, location):
        return location in self.fire_locations

    def __is_person(self, location):
        for person in self.live_people:
            if person.location == location:
                return True
        return False

    def __is_wall(self, location):
        return self.building.text_building['floor1'][location[0]][location[1]] == 'w'

    def __is_stair(self, location):
        return self.building.text_building['floor1'][location[0]][location[1]] == 's'

    def __is_glass(self, location):
        return self.building.text_building['floor1'][location[0]][location[1]] == 'g'

    def __is_empty(self, location):
        return self.building.text_building['floor1'][location[0]][location[1]] == ' '

    def __is_door(self, location):
        return self.building.text_building['floor1'][location[0]][location[1]] == 'd'

    def move(self, person):
        pass