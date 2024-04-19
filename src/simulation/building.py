from .colors import colors, color_codes_html
from copy import deepcopy
from .logger import setup_logger


class Building:
    def __init__(self, simulation, number_of_floors=1):
        building_logger = setup_logger("building_logger", f'../logs/run{simulation.simulation_count}/simulation/building.log', simulation.verbose)
        grid_images_html_logger = setup_logger("grid_images_html_logger", f'../logs/run{simulation.simulation_count}/simulation/grid_image.html', simulation.verbose)
        grid_images_logger = setup_logger("grid_images_logger", f'../logs/run{simulation.simulation_count}/simulation/grid_image.log', simulation.verbose)
        self.building_logger = building_logger
        self.grid_images_html_logger = grid_images_html_logger
        self.grid_images_logger = grid_images_logger
        self.simulation = simulation
        self.number_of_floors = number_of_floors
        self.text = self.__generate_text()
        self.object_locations = {}
        self.color = []
        self.matrix = []
        self.html = ''
        self.grid_image = ''
        self.refresh()
        self.floor_size = len(self.text)
        self.x_size = len(self.text[0])
        self.y_size = len(self.text[0][0])

    def __generate_text(self):
        # w is wall
        # o is obstacle
        # m is mini-object
        # n is normal-object
        # l is large-object
        # d is door
        # s is stair
        # g is glass
        # ' ' is empty space
        # e is for exit
        # p evacuation plan marker
        # 1 is room indicator
        # 2 is wall indicator
        # f is fire
        # b is broken glass

        temp_building = [
            [   # 21 by 31
                ['w','w','g','g','g','g','g','w','w','w','w','w','g','w','w','w','g','w','w','w','g','g','g','g','g','g','g','w','w','w','w'],
                ['w','l','l','l','l','l',' ',' ','w',' ','w','m','n','m','w',' ','m',' ','w','p',' ',' ',' ',' ',' ',' ',' ','p','d','1','e'],
                ['g','l',' ',' ',' ',' ',' ',' ','w',' ','w',' ',' ',' ','w',' ','n','n','w',' ',' ',' ',' ',' ',' ',' ',' ','2','w',' ','w'],
                ['g','l',' ','n','n','n',' ',' ','w',' ','w',' ',' ',' ','w',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w','s','w'],
                ['g','l',' ','n','n','n',' ',' ','w',' ','w',' ','1','p','w','p','1','m','w',' ',' ',' ','w','w','w','w','w','w','w','w','w'],
                ['g',' ',' ',' ',' ',' ',' ',' ','w',' ','w','w','w','d','w','d','w','w','w',' ',' ',' ','w','l','n','l','w',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ','w',' ',' ',' ',' ','1',' ','1',' ',' ','w',' ',' ',' ','w','l','n','l','w',' ',' ',' ','g'],
                ['w','w','w',' ',' ',' ',' ',' ','w',' ','p','1',' ',' ','p',' ',' ',' ','w',' ',' ',' ','w','l','n','l','w',' ',' ',' ','g'],
                ['w',' ','w',' ',' ',' ',' ',' ','w','w','d','w','w','w','d','w','w','w','w',' ',' ',' ',' ',' ',' ',' ','w',' ',' ',' ','g'],
                ['w',' ','w','2',' ',' ',' ',' ',' ',' ','2',' ',' ',' ','2',' ',' ',' ',' ','p',' ',' ',' ',' ',' ','m','w',' ',' ',' ','g'],
                ['e','1','d','p',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','m','w',' ','1','p','w'],
                ['w',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','m','w','w','w','d','w'],
                ['w',' ','w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','2','w'],
                ['w','w','w',' ',' ','2',' ','2',' ',' ',' ',' ',' ',' ',' ','p',' ',' ',' ',' ','p',' ','w','l','n','l','w','l','n','l','w'],
                ['w','w','w','w','w','d','w','d','w','w','w','w','w','w','w',' ','w','w','w','w',' ',' ','w','l','n','l','w','l','n','l','w'],
                ['w',' ',' ',' ','1','p','w','p','1',' ',' ',' ','w',' ','w',' ','w',' ',' ','w',' ',' ','w','l','n','l','w','l','n','l','w'],
                ['g',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ','w',' ','w',' ',' ','w',' ',' ','w','w','w','w','w','w','w','w','w'],
                ['g',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w',' ','w',' ','w',' ',' ','w',' ',' ',' ',' ',' ',' ',' ',' ','w','s','w'],
                ['g',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w','1','w',' ','w','1',' ','w',' ',' ',' ',' ',' ',' ',' ','2','w',' ','w'],
                ['w',' ',' ',' ',' ',' ','w',' ',' ',' ',' ',' ','w','p','d','2','d','p',' ','w','p',' ',' ',' ',' ',' ',' ','p','d','1','e'],
                ['w','w','g','g','g','w','w','w','g','g','g','w','w','w','w','e','w','w','w','w','w','g','g','g','g','g','g','w','w','w','w'],
            ],
            [
                ['w','w','g','g','g','g','g','g','w','w','w','g','g','w','w','w','g','g','w','w','w','g','g','g','g','g','g','w','w','w','w'],
                ['w',' ',' ',' ',' ',' ','m','n','m','w','m','n','m',' ','w','l','l','l',' ','w','p',' ',' ',' ',' ',' ',' ','p','d','1','w'],
                ['g','m',' ',' ','w','1',' ',' ',' ','w',' ',' ',' ','1','w','l',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ','2','w',' ','w'],
                ['g','l',' ',' ','w','p','m','n','m','w','m','n','m','p','w','l',' ',' ',' ','w',' ',' ',' ','2',' ',' ',' ',' ','w','s','w'],
                ['g','l',' ',' ','w','d','w','w','w','w','w','w','w','d','w',' ',' ',' ','l','w',' ',' ','w','d','w','w','w','w','w','w','w'],
                ['w','l',' ','1','w','2',' ',' ',' ',' ',' ',' ',' ','2','w','1',' ',' ','l','w',' ','2','d','p',' ',' ',' ',' ',' ',' ','w'],
                ['w','l','l','p','w',' ',' ',' ',' ','p',' ',' ',' ',' ','w','p','l','l','l','w',' ',' ','w','1','m',' ','m',' ','m',' ','g'],
                ['w','w','w','d','w',' ','w','w','w','w','w','w','w',' ','w','d','w','w','w','w',' ',' ','w',' ','l','l','l','l','l',' ','g'],
                ['w','m','w','2',' ',' ','w',' ',' ',' ',' ',' ','w',' ',' ','2',' ',' ',' ',' ',' ',' ','w',' ','l','l','l','l','l',' ','g'],
                ['g',' ','w',' ',' ',' ','w','2','m','n','m',' ','w','2',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','m',' ','m',' ','m',' ','g'],
                ['g','p','d','2',' ','2','d','p',' ','n',' ','p','d','p',' ',' ',' ',' ',' ',' ','p',' ','w',' ',' ',' ',' ',' ',' ',' ','g'],
                ['w',' ','w',' ',' ',' ','w',' ','m','n','m','1','w',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','m',' ','m',' ','m',' ','g'],
                ['w','m','w','2',' ',' ','w',' ',' ',' ',' ',' ','w',' ',' ','2',' ',' ',' ',' ',' ',' ','w',' ','l','l','l','l','l',' ','g'],
                ['w','w','w','d','w',' ','w','w','w','w','w','w','w',' ','w','d','w','w','w','w',' ',' ','w',' ','l','l','l','l','l',' ','g'],
                ['w','m','1','p','w',' ',' ',' ',' ','p',' ',' ',' ',' ','w','p','l','l','l','w',' ',' ','w','1','m',' ','m',' ','m',' ','g'],
                ['w','n',' ',' ','w','2',' ',' ',' ',' ',' ',' ',' ','2','w','1',' ',' ','l','w',' ','2','d','p',' ',' ',' ',' ',' ',' ','w'],
                ['g','m',' ',' ','w','d','w','w','w','w','w','w','w','d','w',' ',' ',' ','l','w',' ',' ','w','d','w','w','w','w','w','w','w'],
                ['g',' ',' ',' ','w','p','m','n','m','w','m','n','m','p','w','l',' ',' ','l','w',' ',' ',' ','2',' ',' ',' ',' ','w','s','w'],
                ['g',' ',' ',' ','w','1',' ',' ',' ','w',' ',' ',' ','1','w','l',' ',' ',' ','w',' ',' ',' ',' ',' ',' ',' ','2','w',' ','w'],
                ['w','m','n','m','w',' ','m','n','m','w','m','n','m',' ','w','l','l','l',' ','w','p',' ',' ',' ',' ',' ',' ','p','d','1','w'],
                ['w','w','g','w','w','w','g','g','w','w','w','g','g','w','w','w','w','g','w','w','w','g','g','g','g','g','g','w','w','w','w'],
            ],
            [
                ['w','w','w','w','w','g','w','w','w','g','w','w','w','w','w','w','w','w','w','g','w','w','w','g','w','w','w','w','w','w','w'],
                ['w','l','l','w',' ','n',' ','w',' ','n',' ','w',' ','m','w','m',' ','w',' ','n',' ','w',' ','n',' ','w',' ','p','d','1','w'],
                ['g','l',' ','w',' ','n','m','w',' ','n','m','w',' ','n','w','n',' ','w','m','n',' ','w','m','n',' ','w',' ',' ','w',' ','w'],
                ['g','l',' ','w','p','1',' ','w','p','1',' ','w','p','1','w','1','p','w',' ','1','p','w',' ','1','p','w',' ',' ','w','s','w'],
                ['g','l','1','w','d','w','w','w','d','w','w','w','d','w','w','w','d','w','w','w','d','w','w','w','d','w',' ',' ','w','w','w'],
                ['w','l','p','d','2',' ',' ',' ','2',' ',' ',' ','2',' ',' ',' ','2',' ',' ',' ','2',' ',' ',' ','2',' ',' ',' ',' ',' ','w'],
                ['w','w','w','w',' ','p',' ',' ',' ','2',' ','2',' ',' ','p',' ',' ','p',' ',' ','2',' ','2',' ',' ',' ','p',' ',' ','2','w'],
                ['w','m','p','d','2',' ','w','w','w','d','w','d','w','w','w',' ',' ','w','w','w','d','w','d','w','w','w',' ','w','w','d','w'],
                ['g','n','1','w',' ',' ','w',' ','1','p','w','p','1',' ','w',' ',' ','w',' ','1','p','w','p','1',' ','w',' ','w','1','p','w'],
                ['g','m',' ','w',' ',' ','w','1',' ',' ','w',' ',' ','1','w',' ',' ','w','1',' ',' ','w',' ',' ','1','w',' ','w','1','m','g'],
                ['g',' ',' ','w',' ','2','d','p',' ',' ','w',' ',' ','p','d','2','2','d','p',' ',' ','w',' ',' ','p','d','2','d','p','n','g'],
                ['g','m',' ','w',' ',' ','w',' ',' ',' ','w',' ',' ',' ','w',' ',' ','w',' ',' ',' ','w',' ',' ',' ','w',' ','w',' ','m','g'],
                ['g','n','1','w',' ',' ','w',' ','1','p','w','p','1',' ','w',' ',' ','w',' ','1','p','w','p','1',' ','w',' ','w','1','p','w'],
                ['w','m','p','d','2',' ','w','w','w','d','w','d','w','w','w',' ',' ','w','w','w','d','w','d','w','w','w',' ','w','w','d','w'],
                ['w','w','w','w',' ','p',' ',' ',' ','2',' ','2',' ',' ','p',' ',' ','p',' ',' ','2',' ','2',' ',' ',' ','p',' ',' ','2','w'],
                ['w','l','p','d','2',' ',' ',' ','2',' ',' ',' ','2',' ',' ',' ','2',' ',' ',' ','2',' ',' ',' ','2',' ',' ',' ',' ',' ','w'],
                ['g','l','1','w','d','w','w','w','d','w','w','w','d','w','w','w','d','w','w','w','d','w','w','w','d','w',' ',' ','w','w','w'],
                ['g','l',' ','w','p','1',' ','w','p','1',' ','w','p','1','w',' ','p','w',' ','1','p','w',' ','1','p','w',' ',' ','w','s','w'],
                ['g','l',' ','w',' ','n','m','w',' ','n','m','w',' ','n','w','n','1','w','m','n',' ','w','m','n',' ','w',' ','2','w',' ','w'],
                ['w','l','l','w',' ','n',' ','w',' ','n',' ','w',' ','m','w','m',' ','w',' ','n',' ','w',' ','n',' ','w',' ','p','d','1','w'],
                ['w','w','w','w','w','g','w','w','w','g','w','w','w','w','w','w','w','w','w','g','w','w','w','g','w','w','w','w','w','w','w'],
            ],
            # [
            #     ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','d',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w','s','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w','w','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w','w','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w','s','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','w',' ','w'],
            #     ['w',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',',' ',' ',',' ',' ',',' 'd',' ','w'],
            #     ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','e','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
            # ],
        ]
        building = []
        for floor in range(self.number_of_floors):
            building.append(temp_building[floor])
        return building

    def __text_to_colors(self):
        self.building_logger.info("Converting text to colors")
        self.object_locations = {
            "doors": [],
            "exits": [],
            "stairs": [],
            "glasses": [],
            "obstacles": [],
            "walls": [],
            "empties": [],
            "fires": [],
            "broken_glasses": [],
            "exit_plans": [],
        }
        self.color = deepcopy(self.text)
        for floor in range(len(self.color)):
            for row in range(len(self.color[floor])):
                for col in range(len(self.color[floor][row])):
                    cell = self.color[floor][row][col]
                    if cell == 'w':
                        self.object_locations["walls"].append((floor, row, col))
                        cell = colors["wall"]
                    elif cell == 'e':
                        self.object_locations["exits"].append((floor, row, col))
                        cell = colors["exit"]
                    elif cell == 'm' or cell == 'n' or cell == 'l':
                        self.object_locations["obstacles"].append((floor, row, col))
                        cell = colors["object"]
                    elif cell == 's':
                        self.object_locations["stairs"].append((floor, row, col))
                        cell = colors["stair"]
                    elif cell == 'g':
                        self.object_locations["glasses"].append((floor, row, col))
                        cell = colors["glass"]
                    elif cell == 'd':
                        self.object_locations["doors"].append((floor, row, col))
                        cell = colors["door"]
                    elif cell == ' ' or cell == '1' or cell == '2':
                        self.object_locations["empties"].append((floor, row, col))
                        cell = colors["empty"]
                    elif cell == 'f':
                        self.object_locations["fires"].append((floor, row, col))
                        cell = colors["fire"]
                    elif cell == 'b':
                        self.object_locations["broken_glasses"].append((floor, row, col))
                        cell = colors["broken_glass"]
                    elif cell == 'p':
                        self.object_locations["exit_plans"].append((floor, row, col))
                        cell = colors["exit_plan"]
                    self.color[floor][row][col] = cell

    def __text_to_matrix(self):
        # 0 is impassable
        # 1 is easily passable
        # 2 is passable
        # 3 is difficultly passable
        self.building_logger.info("Converting text to pathfinding grid")
        self.matrix = deepcopy(self.text)
        for floor in range(len(self.matrix)):
            for row in range(len(self.matrix[floor])):
                for col in range(len(self.matrix[floor][row])):
                    person = self.simulation.is_person((floor, row, col))
                    cell = self.matrix[floor][row][col]
                    if person:
                        cell = -1
                    elif cell == 'f':
                        cell = -2
                    elif cell == 'w' or cell == 'g' or cell == 'l':
                        cell = -4
                    elif cell == ' ' or cell == 'd' or cell == 'e' or cell == 's' or cell == 'p' or cell == '1' or cell == '2' or cell == 'b':
                        cell = 1
                    elif cell == 'm':
                        cell = 2
                    elif cell == 'n':
                        cell = 3
                    self.matrix[floor][row][col] = cell

    def __test_to_grid_image(self):
        space = "   "
        categories = [
            "wall", "exit", "object", "stair", "glass",
            "door", "empty", "fire", "broken_glass",
            "exit_plan", "follower", "nonfollower"
        ]
        grid_image = ""
        for category in categories:
            color = colors[category] + space
            grid_image += f"{category}: {color}"
            grid_image += colors["reset"] + '\n'
        for floor in range(len(self.color)):
            grid_image += f"Floor {floor}\n"
            grid_image += "   "
            for col in range(len(self.color[floor][0])):
                if col > 9:
                    token = str(col) + " "
                else:
                    token = str(col) + "  "
                grid_image += token
            grid_image += '\n'
            for row in range(len(self.color[floor])):
                for col in range(len(self.color[floor][row])):
                    if col == 0:
                        if row > 9:
                            token = " " + str(row)
                        else:
                            token = "  " + str(row)
                        grid_image += token
                    cost = self.matrix[floor][row][col]
                    if cost < 0:
                        cost = " " + str(cost)
                    else:
                        cost = "  " + str(cost)
                    person = self.simulation.is_person((floor, row, col))
                    token = self.color[floor][row][col]
                    if person:
                        token = person.color
                    grid_image += token + cost
                grid_image += "" + colors["reset"] + '\n'
        grid_image += '\n'
        self.grid_image = grid_image

    def refresh(self):
        self.building_logger.info("Refreshing building")
        self.__text_to_colors()
        self.__text_to_matrix()
        self.__text_to_html()
        self.__test_to_grid_image()
        self.building_logger.info(self.color)
        self.building_logger.info(self.matrix)
        self.building_logger.info(self.object_locations)
        self.building_logger.info(self.text)
        self.grid_images_html_logger.info(self.html)
        self.grid_images_logger.info(self.grid_image)
        print(self.grid_image)

    def __text_to_html(self):
        self.html = ''
        for floor in range(self.number_of_floors):
            self.html += '<div>\n'
            self.html += f"<h1>Floor {floor}</h1>\n"
            for x in range(len(self.text[floor])):
                for y in range(len(self.text[floor][x])):
                    location = (floor, x, y)
                    person = self.simulation.is_person(location)
                    if person:
                        c = 'fo' if person.likes_people else 'nf'
                    else:
                        c = self.text[floor][x][y]
                    color_code = color_codes_html[c]
                    self.html += f"<span style='color:{color_code};'>   </span>"
                self.html += '\n'
            self.html += '</div>\n'
        self.html += '\n'
