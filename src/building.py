# Black : Wall
# White : Empty
# Light Brown : Window
# Brown : Door
# Dark Brown : Exit
# Stair Blue : Stair

# Light Grey : Small Obstacle
# Grey : Normal Obstacle
# Dark Grey : Large Obstacle

# Red : Fire
# Light Red : Shooter

# Blue : Copycat
# Teal : Cheater
# Pink : Cooperator
# Yellow : Grudger
# Orange : Detective
# Tan : Copykitten
# Green : Simpleton
# Purple : Random

# auto generate a building with glass, doors, stairs, and obstacles

# w = wall
# e = exit
# o = obstacle
# s = stair
# g = glass
# d = door
# ' ' = empty

from colors import colors


def convert_text_to_colors(building):
    for floor in building:
        for row in floor:
            for i in range(len(row)):
                if row[i] == 'w':
                    row[i] = colors["Black"]
                elif row[i] == 'e':
                    row[i] = colors["Dark Brown"]
                elif row[i] == 'o':
                    row[i] = colors["Grey"]
                elif row[i] == 's':
                    row[i] = colors["Stair Blue"]
                elif row[i] == 'g':
                    row[i] = colors["Light Brown"]
                elif row[i] == 'd':
                    row[i] = colors["Brown"]
                elif row[i] == ' ':
                    row[i] = colors["White"]
