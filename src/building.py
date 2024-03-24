# TODO change the building to be a 3D array not a dictionary

from colors import object_colors


class Building:
    def __init__(self):
        self.text_building = self.generate_building()
        self.object_locations = {
            "door": [],
            "exit": [],
            "stair": [],
            "glass": [],
            "obstacle": [],
            "wall": [],
            "empty": [],
        }
        self.color_building = self.convert_text_to_colors(self.text_building)

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

        building = {
            'floor_count': 2,
            'floor_square_area': 20,
            'floor1': [
                ['w','w','w','w','w','w','w','w','w','e','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
                ['w','l','l','l','l','l',' ',' ','h',' ','w','s','n','s','w',' ','s',' ','w',' ',' ',' ',' ','s','w'],
                ['w','l',' ',' ',' ',' ',' ',' ','h',' ','w',' ',' ',' ','w',' ','n','n','w',' ',' ',' ','w','w','w'],
                ['w','l',' ','n','n','n',' ',' ','h',' ','w',' ',' ',' ','w',' ',' ',' ','w',' ',' ',' ','e'],
                ['w','l',' ','n','n','n',' ',' ','h',' ','w',' ',' ',' ','w',' ',' ','s','w',' ',' ',' ','w','w','w','w','w','w','w','w','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ','h',' ','w','w','w',' ','w',' ','w','w','w',' ',' ',' ','h','l','n','l','w',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ',' ',' ','h','l','n','l','w',' ',' ',' ','w'],
                ['w','w','w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ',' ',' ','h','l','n','l','w',' ',' ',' ','w'],
                ['w',' ','w',' ',' ',' ',' ',' ','w','w',' ','w','w','w',' ','w','w','w','w',' ',' ',' ',' ',' ',' ',' ','h',' ',' ',' ','w'],
                ['w',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','s','h',' ',' ',' ','w'],
                ['e',' ','e',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','s','h',' ',' ',' ','w'],
                ['w',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','s','h',' ',' ',' ','w'],
                ['w',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w','w','w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','h','l','n','l','h','l','n','l','w'],
                ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w',' ','w','w','w','w',' ',' ','h','l','n','l','h','l','n','l','w'],
                ['w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ','w',' ','w',' ',' ','w',' ',' ','h','l','n','l','h','l','n','l','w'],
                ['w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ','w',' ','w',' ',' ','w',' ',' ','w','w','w','w','w','w','w','w','w'],
                ['w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ','w',' ','w',' ',' ','w',' ',' ','e'],
                ['w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ','w',' ','w',' ',' ','w',' ',' ','w','w','w'],
                ['w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ',' ','w',' ',' ',' ','s','w'],
                ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w',' ','w','w','w','w','w','w','w','w','w'],
            ],
            'floor2': [
                ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'e', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
                ['d', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['d', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['d', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
                ['d', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
            ]
        }
        return building

    def convert_text_to_colors(self, text_building):
        color_building = text_building.copy()
        floors = color_building.values()
        for floor in range(len(floors)):
            for row in floors[floor]:
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
        return color_building
