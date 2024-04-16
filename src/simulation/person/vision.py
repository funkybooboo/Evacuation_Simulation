from .memory import Memory


class Vision:
    def __init__(self, simulation, person):
        self.simulation = simulation
        self.person = person

    def look_around(self):
        what_is_around = Memory()
        location = (self.person.location[1], self.person.location[2])
        self.__search(location, self.person.visibility, what_is_around, [])
        return what_is_around

    def __search(self, location, visibility, what_is_around, blocked):
        if visibility <= 0:
            return
        if location in blocked:
            return
        x = location[0]
        y = location[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.__is_out_of_bounds(x + i, y + j) or self.__is_blocked(blocked, x, y):
                    continue
                self.__add_to_memory(blocked, i, j, what_is_around, x, y)
                self.__search((x + i, y + j), visibility - 1, what_is_around, blocked)

    def __is_out_of_bounds(self, x, y):
        return 0 > x >= self.simulation.building.x_size or 0 > y >= self.simulation.building.y_size

    def __add_to_memory(self, blocked, i, j, what_is_around, x, y):
        location = (self.person.location[0], x + i, y + j)
        self.simulation.is_in_building(location)
        if self.simulation.is_wall(location):
            what_is_around.add("walls", location)
            self.__block(blocked, i, j, x, y)
        elif self.simulation.is_door(location):
            what_is_around.add("doors", location)
        elif self.simulation.is_exit(location):
            what_is_around.add("exits", location)
        elif self.simulation.is_stair(location):
            what_is_around.add("stairs", location)
        elif self.simulation.is_glass(location):
            what_is_around.add("glasses", location)
        elif self.simulation.is_mini_obstacle(location):
            what_is_around.add("obstacles", location)
        elif self.simulation.is_normal_obstacle(location):
            what_is_around.add("obstacles", location)
        elif self.simulation.is_large_obstacle(location):
            self.__block(blocked, i, j, x, y)
            what_is_around.add("broken_glasses", location)
        elif self.simulation.is_empty(location):
            what_is_around.add("empties", location)
        elif location in self.simulation.fire_locations:
            what_is_around.add("fires", location)
        elif self.simulation.is_person(location):
            what_is_around.add("people", location)
        elif self.simulation.is_broken_glass(location):
            what_is_around.add("broken_glasses", location)
        elif self.simulation.is_room(location):
            self.room_type = "room"
        elif self.simulation.is_hallway(location):
            self.room_type = "hall"
        elif self.simulation.is_exit_plan(location):
            what_is_around.add("exit_plans", location)
        else:
            raise Exception(f"I see a char you didn't tell me about: {self.simulation.building.text[self.person.location[0]][x + i][y + j]}")

    def __block(self, blocked, i, j, x, y):
        x = x + i
        y = y + j
        if not self.__is_diagonal(i, j):
            blocked.append((x, y))
            direction = self.__get_direction(i, j)
            if direction == 'l':
                for k in range(x, 0, -1):
                    blocked.append((x + k, y))
            elif direction == 'r':
                for k in range(x, self.simulation.building.x_size):
                    blocked.append((x + k, y))
            elif direction == 'd':
                for k in range(y, self.simulation.building.y_size):
                    blocked.append((x, y + k))
            elif direction == 'u':
                for k in range(y, 0, -1):
                    blocked.append((x, y + k))

    @staticmethod
    def __is_blocked(blocked, x, y):
        return (x, y) in blocked

    @staticmethod
    def __is_diagonal(i, j):
        return i < 0 < j or j < 0 < i or (i < 0 and j < 0) or (i > 0 and j > 0)

    @staticmethod
    def __get_direction(i, j):
        if i == 0 and j == 1:
            return 'u'
        if i == 0 and j == -1:
            return 'd'
        if i == 1 and j == 0:
            return 'r'
        if i == -1 and j == 0:
            return 'l'
        else:
            raise Exception('invalid coordinates')
