from .memory import Memory


class Vision:
    def __init__(self, person):
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
        blocked.append((x, y))
        for i in range(-1, 2):
            for j in range(-1, 2):
                a = x + i
                b = y + j
                if self.__is_out_of_bounds(a, b) or self.__is_blocked(blocked, a, b):
                    continue
                self.__add_to_memory(what_is_around, blocked, i, j, a, b)
                self.__search((a, b), visibility - 1, what_is_around, blocked)

    def __add_to_memory(self, what_is_around, blocked, i, j, a, b):
        location = (self.person.location[0], a, b)
        self.person.simulation.is_not_in_building(location)
        if self.person.simulation.is_wall(location):
            what_is_around.add("walls", location)
            self.__block(blocked, i, j, a, b)
        elif self.person.simulation.is_door(location):
            what_is_around.add("doors", location)
        elif self.person.simulation.is_exit(location):
            what_is_around.add("exits", location)
        elif self.person.simulation.is_stair(location):
            what_is_around.add("stairs", location)
        elif self.person.simulation.is_glass(location):
            what_is_around.add("glasses", location)
        elif self.person.simulation.is_mini_obstacle(location):
            what_is_around.add("obstacles", location)
        elif self.person.simulation.is_normal_obstacle(location):
            what_is_around.add("obstacles", location)
        elif self.person.simulation.is_large_obstacle(location):
            self.__block(blocked, i, j, a, b)
            what_is_around.add("broken_glasses", location)
        elif self.person.simulation.is_empty(location):
            what_is_around.add("empties", location)
        elif location in self.person.simulation.fire_locations:
            what_is_around.add("fires", location)
        elif self.person.simulation.is_person(location):
            what_is_around.add("people", location)
        elif self.person.simulation.is_broken_glass(location):
            what_is_around.add("broken_glasses", location)
        elif self.person.simulation.is_room(location):
            self.room_type = "room"
        elif self.person.simulation.is_hallway(location):
            self.room_type = "hall"
        elif self.person.simulation.is_exit_plan(location):
            what_is_around.add("exit_plans", location)
        else:
            raise Exception(f"I see a char you didn't tell me about: {self.person.simulation.building.text[self.person.location[0]][a][b]}")

    def __is_out_of_bounds(self, x, y):
        return x < 0 or y < 0 or x >= self.person.simulation.building.x_size or y >= self.person.simulation.building.y_size

    def __block(self, blocked, i, j, a, b):
        blocked.append((a, b))
        if not self.__is_diagonal(i, j):
            direction = self.__get_direction(i, j)
            if direction == 'l':
                for k in range(a, 0, -1):
                    blocked.append((a + k, b))
            elif direction == 'r':
                for k in range(a, self.person.simulation.building.x_size):
                    blocked.append((a + k, b))
            elif direction == 'd':
                for k in range(b, self.person.simulation.building.y_size):
                    blocked.append((a, b + k))
            elif direction == 'u':
                for k in range(b, 0, -1):
                    blocked.append((a, b + k))

    @staticmethod
    def __is_blocked(blocked, x, y):
        return (x, y) in blocked

    @staticmethod
    def __is_diagonal(i, j):
        return i < 0 < j or j < 0 < i or (i < 0 and j < 0) or (i > 0 and j > 0)

    @staticmethod
    def __get_direction(i, j):
        if i == 0 and j == 1:
            return 'r'
        if i == 0 and j == -1:
            return 'l'
        if i == 1 and j == 0:
            return 'u'
        if i == -1 and j == 0:
            return 'd'
        else:
            raise Exception('invalid coordinates')
