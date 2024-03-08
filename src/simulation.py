from building import building
from person import Person
from random import randint


class Simulation:
    def __init__(self, number_of_people, verbose):
        self.number_of_people = number_of_people
        self.verbose = verbose
        self.building = building
        self.live_people = self.__generate_people()
        self.dead_people = []
        self.fire_locations = [(randint(0, len(self.building['floor1']) - 1), randint(0, len(self.building['floor1'][0]) - 1))]
        self.statistics()

    def __generate_people(self):
        people = []
        for i in range(self.number_of_people):
            people.append(Person(f'Person{i}', i, 20, 5, 5, 'blue', 5, 5, 5))
        return people

    def print_building(self):
        for floor in self.building:
            for row in floor:
                for cell in row:
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
            for person in self.live_people:
                for fire_location in self.fire_locations:
                    if person.location == fire_location:
                        if self.verbose:
                            print(f"{person.name} has been caught in the fire")
                        self.number_of_people -= 1
                        self.dead_people.append(person)
                        self.live_people.remove(person)

                move_data = self.move(person)
                if move_data['is_hit']:
                    person1 = self.live_people[move_data['pk1']]
                    person2 = self.live_people[move_data['pk2']]
                    if self.verbose:
                        print(f"{person1.name} and {person2.name} have collided")
                    self.compete(person1, person2)
                if move_data['is_exit']:
                    self.number_of_people -= 1
                    self.live_people.remove(person)
                    if self.verbose:
                        print(f"{person.name} has exited the building")
            if self.verbose:
                print(f"{self.number_of_people} people remaining")
            for fire_location in self.fire_locations:
                if self.is_fire_spread():
                    self.fire_locations.append((fire_location[0], fire_location[1] + 1))
                if self.is_fire_spread():
                    self.fire_locations.append((fire_location[0], fire_location[1] - 1))
                if self.is_fire_spread():
                    self.fire_locations.append((fire_location[0] + 1, fire_location[1]))
                if self.is_fire_spread():
                    self.fire_locations.append((fire_location[0] - 1, fire_location[1]))
        if self.verbose:
            print("Evacuation complete")
        self.statistics()

    @staticmethod
    def is_fire_spread():
        return randint(0, 10) == 1

    def compete(self, person1, person2):
        pass

    def path_find(self, person):
        pass

    def move(self, person):
        pass

