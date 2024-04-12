from sys import argv
from simulation import Simulation
from os import mkdir


def main(args):
    n = -1
    with open('run', 'rw') as f:
        n = int(f.read())
        f.write(str(n+1))
    if n == -1:
        raise Exception("Error reading run file")
    # make a directory for the run
    mkdir(f'../logs/run{n}')
    number_of_people = 100
    verbose = False
    with_ai = False
    if len(args > 1) and args[0].isdigit():
        number_of_people = int(args[1])
    if len(args) > 2 and (args[1] == "-v" or args[1] == "--verbose"):
        verbose = True
    if len(args) > 3 and (args[2] == "-ai" or args[2] == "--ai"):
        with_ai = True
    simulation = Simulation(number_of_people, n, verbose, with_ai)
    simulation.statistics()
    simulation.evacuate()
    simulation.statistics()


if __name__ == '__main__':
    main(argv[1:])
