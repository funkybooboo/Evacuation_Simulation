class Memory:

    def __init__(self):
        self.doors = set()
        self.exits = set()
        self.stairs = set()
        self.glasses = set()
        self.obstacles = set()
        self.walls = set()
        self.empties = set()
        self.fires = set()
        self.people = set()
        self.broken_glass = set()
        self.exit_plans = set()
        self.items = ['doors', 'exits', 'stairs', 'glasses', 'obstacles', 'walls', 'empties', 'fires', 'people', 'broken_glass', 'exit_plans']

    def combine(self, other):
        for item in self.items:
            for location in getattr(other, item):
                self.add(item, location)

    def add(self, what, where):
        if what is None or where is None:
            return
        if what not in self.items:
            return
        for item in self.items:
            if item != what:
                self.__remove(item, where)
        getattr(self, what).add(where)

    def __remove(self, what, where):
        if what is None or where is None:
            return
        if what not in self.items:
            return
        if where in getattr(self, what):
            getattr(self, what).remove(where)

    def __str__(self):
        return f"Doors: {self.doors}\nExits: {self.exits}\nStairs: {self.stairs}\nGlasses: {self.glasses}\nObstacles: {self.obstacles}\nWalls: {self.walls}\nEmpties: {self.empties}\nFires: {self.fires}\nPeople: {self.people}\nBroken Glass: {self.broken_glass}\nExit Plans: {self.exit_plans}"
