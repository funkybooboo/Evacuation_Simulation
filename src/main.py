from sys import argv
from simulation import Simulation


def main(args):
    number_of_people = 100
    verbose = False
    with_ai = False
    if len(args > 1) and args[0].isdigit():
        number_of_people = int(args[1])
    if len(args) > 2 and (args[1] == "-v" or args[1] == "--verbose"):
        verbose = True
    if len(args) > 3 and (args[2] == "-ai" or args[2] == "--ai"):
        with_ai = True
    simulation = Simulation(number_of_people, verbose, with_ai)
    simulation.statistics()
    simulation.evacuate()
    simulation.statistics()


if __name__ == '__main__':
    main(argv[1:])
