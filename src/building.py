from colors import object_colors


class Building:
    def __init__(self, simulation):
        self.simulation = simulation
        self.text_building = self.generate_building()
        self.object_locations = {
            "door": [],
            "exit": [],
            "stair": [],
            "glass": [],
            "obstacle": [],
            "wall": [],
            "empty": [],
            "fire": [],
        }
        self.color_building = []
        self.convert_text_to_colors()

    @staticmethod
    def generate_building():
        # w is wall
        # h is half-wall
        # o is obstacle
        # m is mini-object
        # n is normal-object
        # l is large-object
        # d is door
        # s is stair
        # g is glass
        # ' ' is empty space
        # e is for exit

        building = [
            [
                ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
                ['w','l','l','l','l','l',' ',' ','h',' ','w','s','n','s','w',' ','s',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','d',' ','e'],
                ['w','l',' ',' ',' ',' ',' ',' ','h',' ','w',' ',' ',' ','w',' ','n','n','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','w'],
                ['w','l',' ','n','n','n',' ',' ','h',' ','w',' ',' ',' ','w',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w','s','w'],
                ['w','l',' ','n','n','n',' ',' ','h',' ','w',' ',' ',' ','w',' ',' ','s','w',' ',' ',' ','w','w','w','w','w','w','w','w','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ','h',' ','w','w','w','d','w','d','w','w','w',' ',' ',' ','h','l','n','l','w',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ',' ',' ','h','l','n','l','w',' ',' ',' ','w'],
                ['w','w','w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ',' ',' ','h','l','n','l','w',' ',' ',' ','w'],
                ['w',' ','w',' ',' ',' ',' ',' ','w','w','d','w','w','w','d','w','w','w','w',' ',' ',' ',' ',' ',' ',' ','h',' ',' ',' ','w'],
                ['w',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','s','h',' ',' ',' ','w'],
                ['e',' ','d',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','s','h',' ',' ',' ','w'],
                ['w',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','s','h','h','h','d','w'],
                ['w',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w','w','w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','h','l','n','l','h','l','n','l','w'],
                ['w','w','w','w','w','d','w','d','w','w','w','w','w','w','w',' ','w','w','w','w',' ',' ','h','l','n','l','h','l','n','l','w'],
                ['w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ','w',' ','w',' ',' ','w',' ',' ','h','l','n','l','h','l','n','l','w'],
                ['w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ','w',' ','w',' ',' ','w',' ',' ','w','w','w','w','w','w','w','w','w'],
                ['w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ','w',' ','w',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ','w','s','w'],
                ['w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ','w',' ','w',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','w'],
                ['w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ','d',' ','d',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ','d',' ','e'],
                ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','e','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
            ],
            [
                ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
                ['w',' ',' ',' ',' ',' ','s','n','s','w','s','n','s',' ','w','l','l','l',' ','w',' ',' ',' ',' ',' ',' ',' ',' ','d',' ','w'],
                ['w','s',' ',' ','w',' ',' ',' ',' ','w',' ',' ',' ',' ','w','l',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','w'],
                ['w','l',' ',' ','w',' ','s','n','s','w','s','n','s',' ','w','l',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ','w','s','w'],
                ['w','l',' ',' ','w','d','w','w','w','w','w','w','w','d','w',' ',' ',' ','l','w',' ',' ','w','d','w','w','w','w','w','w','w'],
                ['w','l',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ',' ',' ','l','w',' ',' ','d',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w','l','l',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','l','l','l','w',' ',' ','w',' ','s',' ','s',' ','s',' ','w'],
                ['w','w','w','d','w',' ','w','w','w','w','w','w','w',' ','w','d','w','w','w','w',' ',' ','w',' ','l','l','l','l','l',' ','w'],
                ['w','s','w',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','l','l','l','l','l',' ','w'],
                ['w',' ','w',' ',' ',' ','w',' ','s','n','s',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','s',' ','s',' ','s',' ','w'],
                ['w',' ','d',' ',' ',' ','d',' ',' ','n',' ',' ','d',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ','w',' ',' ',' ','w',' ','s','n','s',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','s',' ','s',' ','s',' ','w'],
                ['w','s','w',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','l','l','l','l','l',' ','w'],
                ['w','w','w','d','w',' ','w','w','w','w','w','w','w',' ','w','d','w','w','w','w',' ',' ','w',' ','l','l','l','l','l',' ','w'],
                ['w','s',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','l','l','l','w',' ',' ','w',' ','s',' ','s',' ','s',' ','w'],
                ['w','n',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ',' ',' ','l','w',' ',' ','d',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w','s',' ',' ','w','d','w','w','w','w','d','w','w','w','w',' ',' ',' ','l','w',' ',' ','w','d','w','w','w','w','w','w','w'],
                ['w',' ',' ',' ','w',' ','s','n','s','w','s','n','s',' ','w','l',' ',' ','l','w',' ',' ',' ',' ',' ',' ',' ',' ','w','s','w'],
                ['w',' ',' ',' ','w',' ',' ',' ',' ','w',' ',' ',' ',' ','w','l',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','w'],
                ['w','s','n','s','w',' ','s','n','s','w','s','n','s',' ','w','l','l','l',' ','w',' ',' ',',' ',' ',',' ',' ',',' 'd',' ','w'],
                ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','e','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
            ]
        ]
        return building

    def convert_text_to_colors(self):
        self.object_locations = {
            "door": [],
            "exit": [],
            "stair": [],
            "glass": [],
            "obstacle": [],
            "wall": [],
            "empty": [],
            "fire": [],
        }
        self.color_building = self.text_building.copy()
        floors = len(self.color_building)
        for floor in range(floors):
            for row in self.color_building[floor]:
                for col in range(len(row)):
                    if row[col] == 'w' or row[col] == 'h':
                        self.object_locations["wall"].append((floor, row, col))
                        row[col] = object_colors["Black"]
                    elif row[col] == 'e':
                        self.object_locations["exit"].append((floor, row, col))
                        row[col] = object_colors["Dark Brown"]
                    elif row[col] == 's' or row[col] == 'n' or row[col] == 'l':
                        self.object_locations["obstacle"].append((floor, row, col))
                        row[col] = object_colors["Grey"]
                    elif row[col] == 's':
                        self.object_locations["stair"].append((floor, row, col))
                        row[col] = object_colors["Stair Blue"]
                    elif row[col] == 'g':
                        self.object_locations["glass"].append((floor, row, col))
                        row[col] = object_colors["Light Brown"]
                    elif row[col] == 'd':
                        self.object_locations["door"].append((floor, row, col))
                        row[col] = object_colors["Brown"]
                    elif row[col] == ' ':
                        self.object_locations["empty"].append((floor, row, col))
                        row[col] = object_colors["White"]
                    elif row[col] == 'f':
                        self.object_locations["fire"].append((floor, row, col))
                        row[col] = object_colors["Red"]

    def print_building(self):
        self.convert_text_to_colors()
        for floor in range(len(self.color_building)):
            for row in range(self.color_building[floor]):
                for col in range(self.color_building[floor][row]):
                    person = self.simulation.__is_person((floor, row, col))
                    if person:
                        print(person.color)
                    else:
                        print(self.color_building[floor][row][col])
