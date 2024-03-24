from person import Person
from random import randint


class Simulation:
    def __init__(self, number_of_people, verbose, building):
        self.number_of_people = number_of_people
        self.verbose = verbose
        self.building = building
        self.live_people = self.__generate_people()
        self.dead_people = []
        self.fire_locations = [
            (randint(0, len(self.building['floor1']) - 1), randint(0, len(self.building['floor1'][0]) - 1))]

    def __generate_people(self):
        people = []
        for i in range(self.number_of_people):
            people.append(Person(f'Person{i}', i, 20, 5, 5, 'blue', 5, 5, 5))
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
            for fire_location in self.fire_locations:
                if person.location == fire_location:
                    if self.verbose:
                        print(f"{person.name} has been caught in the fire")
                    self.number_of_people -= 1
                    self.dead_people.append(person)
                    self.live_people.remove(person)

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
            return True
        else:
            return False

    def get_normal_form_game(self, person1, person2):
        base_payoffs = {
            ("cooperate", "cooperate"): (3, 3),
            ("cooperate", "defect"): (0, 5),
            ("defect", "cooperate"): (5, 0),
            ("defect", "defect"): (1, 1),
        }
        return base_payoffs[(person1.strategy, person2.strategy)]

    def __get_next_best_location(self, person):
        pass

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
        return self.building['floor1'][location[0]][location[1]] == 'w'

    def __is_stair(self, location):
        return self.building['floor1'][location[0]][location[1]] == 's'

    def __is_glass(self, location):
        return self.building['floor1'][location[0]][location[1]] == 'g'

    def __is_empty(self, location):
        return self.building['floor1'][location[0]][location[1]] == ' '

    def __is_door(self, location):
        return self.building['floor1'][location[0]][location[1]] == 'd'

    def __closest_exit(self, location):
        pass

    def __closest_stair(self, location):
        pass

    def __closest_door(self, location):
        pass

    def move(self, person):
        path = self.__get_next_best_location(person)
