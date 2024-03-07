class Simulation:
    def __init__(self, number_of_people, verbose):
        self.number_of_people = number_of_people
        self.verbose = verbose

    def statistics(self):
        if self.verbose:
            print(f"Number of people: {self.number_of_people}")

    def evacuate(self):
        if self.verbose:
            print("Evacuating...")
