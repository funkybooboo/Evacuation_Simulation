# auto generate a building with glass, doors, stairs, and obstacles

# w = wall
# e = exit
# o = obstacle
# s = stair
# g = glass
# d = door
# ' ' = empty

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
        return {
            "floor1": [
                [''],
            ],
            "floor2": [
                [''],
            ],
        }

    def convert_text_to_colors(self, text_building):
        color_building = text_building.copy()
        floors = color_building.values()
        for floor in range(len(floors)):
            for row in floors[floor]:
                for col in range(len(row)):
                    if row[col] == 'w':
                        self.object_locations["wall"].append((floor, row, col))
                        row[col] = object_colors["Black"]
                    elif row[col] == 'e':
                        self.object_locations["exit"].append((floor, row, col))
                        row[col] = object_colors["Dark Brown"]
                    elif row[col] == 'o':
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
