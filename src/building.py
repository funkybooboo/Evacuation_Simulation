

# auto generate a building with glass, doors, stairs, and obstacles

# w = wall
# e = exit
# o = obstacle
# s = stair
# g = glass
# d = door
# ' ' = empty

from colors import object_colors


def convert_text_to_colors(building):
    for floor in building:
        for row in floor:
            for i in range(len(row)):
                if row[i] == 'w':
                    row[i] = object_colors["Black"]
                elif row[i] == 'e':
                    row[i] = object_colors["Dark Brown"]
                elif row[i] == 'o':
                    row[i] = object_colors["Grey"]
                elif row[i] == 's':
                    row[i] = object_colors["Stair Blue"]
                elif row[i] == 'g':
                    row[i] = object_colors["Light Brown"]
                elif row[i] == 'd':
                    row[i] = object_colors["Brown"]
                elif row[i] == ' ':
                    row[i] = object_colors["White"]
