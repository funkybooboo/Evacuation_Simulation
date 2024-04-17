from random import randint
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder
from copy import deepcopy
from src.simulation.logger import setup_logger


class Movement:
    def __init__(self, person):
        self.logger = setup_logger("movement_logger", f'../logs/run{person.simulation.simulation_count}/people/person{person.pk}/movement.log', person.simulation.verbose)
        self.person = person

    def run(self):
        self.logger.info(f"Moving starting at {self.person.location}")
        if self.person.fear == self.person.simulation.max_fear:
            self.person.number_of_max_fear += 1
        other = None
        for _ in range(self.person.speed):
            if self.person.is_dead():
                break
            self.person.memory.combine(self.person.vision.look_around())
            other = self.__step()
            # hit person
            if other:
                break
            # in a fire
            if self.person.location in self.person.simulation.fire_locations:
                self.person.health -= 25
                self.person.end_turn_in_fire = True
                self.person.number_of_fire_touches += 1
            else:
                self.person.end_turn_in_fire = False
            # at a stair
            if self.person.simulation.is_stair(self.person.location):
                self.person.location = (self.person.location[0] - 1, self.person.location[1], self.person.location[2])
            # at an exit
            if self.person.simulation.is_exit(self.person.location):
                break
            if self.person.simulation.is_broken_glass(self.person.location):
                break
        self.logger.info(f"{self.person.name} is at {self.person.location}")
        return other

    def __step(self):
        return self.person.thinker.think()

    def get_time_to_get_out(self):
        long_time = -1
        closest_exit = self.get_closest(self.person.location, self.person.memory.exits)
        if closest_exit:
            d = self.get_distance(self.person.location, closest_exit)
            if not d:
                return long_time
            number_of_people = self.person.get_number_of_people_near()
            return number_of_people + d
        return long_time

    def follow_evacuation_plan(self):
        closest_exit_plan = self.get_closest(self.person.location, self.person.memory.exit_plans)
        closest_exit = self.get_closest(closest_exit_plan, self.person.simulation.building.object_locations["exits"])
        return self.towards(closest_exit)

    def explore(self):
        if self.person.is_in_room():
            closest_door = self.get_closest(self.person.location, self.person.memory.doors)
            if closest_door:
                return self.towards(closest_door)
        furthest_empty = self.get_furthest(self.person.location, self.person.memory.empties)
        if furthest_empty:
            return self.towards(furthest_empty)
        return self.randomly()

    def randomly(self):
        for i in range(8):
            x = randint(-1, 1)
            y = randint(-1, 1)
            new_location = (self.person.location[0], self.person.location[1] + x, self.person.location[2] + y)
            if self.person.simulation.is_valid_location_for_person(new_location):
                return self.person.place(new_location)
        return None

    def towards(self, location):
        if location is None:
            return None
        self.person.simulation.is_not_in_building(location)
        floor1 = self.person.location[0]
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
                n_x = node.y
                n_y = node.x
                break
        if not n_x or not n_y:
            return None
        new_location = (floor1, n_x, n_y)
        return self.person.place(new_location)

    def get_path(self, location, grid):
        if location is None:
            raise Exception("location is None")
        if grid is None:
            raise Exception("grid is None")
        self.person.simulation.is_not_in_building(self.person.location)
        self.person.simulation.is_not_in_building(location)
        x1 = self.person.location[1]
        y1 = self.person.location[2]
        start = grid.node(y1, x1)
        x2 = location[1]
        y2 = location[2]
        end = grid.node(y2, x2)
        finder = DijkstraFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, grid)
        self.logger.info(f'operations:', runs, 'path length:', len(path))
        self.logger.info(grid.grid_str(path=path, start=start, end=end))
        return path

    def get_grid(self, i):
        floor = self.person.location[0]
        matrix = deepcopy(self.person.simulation.building.matrix[floor])
        if i == 0:
            self.__switcher(matrix, -1, -2)
        elif i == 1:
            self.__switcher(matrix, 3, -2)
        elif i == 2:
            self.__switcher(matrix, -1, 5)
        elif i == 3:
            self.__switcher(matrix, 3, 5)
        else:
            raise Exception("invalid i")
        grid = Grid(matrix=matrix)
        return grid

    @staticmethod
    def __switcher(matrix, p, f):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == -1:
                    matrix[row][col] = p
                elif matrix[row][col] == -2:
                    matrix[row][col] = f

    def get_closest(self, location1, lst):
        """
        get the closet of something from a list. ex: get the closest wall, get the closest person, etc.
        """
        if len(lst) == 0:
            return None
        closest = next(iter(lst))
        for location2 in lst:
            if location1[0] != location2[0]:
                continue
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
