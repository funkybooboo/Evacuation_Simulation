from .memory import Memory


class Vision:
    def __init__(self, simulation, person):
        self.simulation = simulation
        self.person = person

    def look_around(self):
        what_is_around = Memory()
        self.__search(self.person.location, self.person.visibility, what_is_around, [], [])
        return what_is_around

    def __search(self, location, visibility, what_is_around, blocked, been_there):
        if visibility <= 0:
            return
        if location in been_there:
            return
        been_there.append(location)
        floor = location[0]
        x = location[1]
        y = location[2]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.__is_continue(x + i, y + j, blocked):
                    continue
                self.__add_to_memory(blocked, floor, i, j, what_is_around, x, y)
                self.__search((floor, x + i, y + j), visibility - 1, what_is_around, blocked, been_there)

    def __is_continue(self, x, y, blocked):
        return 0 > x >= self.simulation.building.x_size or 0 > y >= self.simulation.building.y_size or self.__is_blocked(blocked, x, y)

    def __add_to_memory(self, blocked, floor, i, j, what_is_around, x, y):
        location = (floor, x + i, y + j)
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
            raise Exception(f"I see a char you didn't tell me about: {self.simulation.building.text[floor][x + i][y + j]}")

    def __block(self, blocked, i, j, x, y):
        if not self.__is_diagonal(i, j):
            blocked.append((x + i, y + j, self.__get_letter(i, j)))

    def __is_blocked(self, blocked, x, y):
        left = 0
        top = 0
        right = self.simulation.building.x_size
        bottom = self.simulation.building.y_size
        for block in blocked:
            b_x = block[0]
            b_y = block[1]
            letter = block[2]
            if y == b_y or x == b_x:
                if letter == 'l':
                    for k in range(left, b_x):
                        if x == k:
                            return True
                elif letter == 'r':
                    for k in range(b_x, right):
                        if x == k:
                            return True
                elif letter == 'd':
                    for k in range(b_y, bottom):
                        if y == k:
                            return True
                elif letter == 'u':
                    for k in range(top, b_y):
                        if y == k:
                            return True
        return False

    @staticmethod
    def __is_diagonal(i, j):
        return i < 0 < j or j < 0 < i or (i < 0 and j < 0) or (i > 0 and j > 0)

    @staticmethod
    def __get_letter(i, j):
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
