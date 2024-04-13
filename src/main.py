from sys import argv
from simulation import Simulation
from os import mkdir
import logging


def main(args):

    # create log directory
    with open('run', 'r') as f:
        n = int(f.read())
    with open('run', 'w') as f:
        f.write(str(n + 1))
    mkdir(f'../logs/run{n}')

    # set up logging
    logging.basicConfig(filename=f'../logs/run{n}/main.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # default values
    number_of_people = 100
    verbose = False
    with_ai = False
    # number of seconds for firefights to arrive
    time_for_firefights = 1000
    fire_spread_rate = 0.2
    max_visibility = 5
    min_visibility = 1
    max_strength = 10
    min_strength = 1
    max_speed = 5
    min_speed = 1
    max_fear = 10
    min_fear = 1
    max_age = 80
    min_age = 10
    max_health = 100
    min_health = 80
    follower_probability = 0.5

    # parse arguments from command line
    if len(args) > 1 and args[0].isdigit():
        number_of_people = int(args[1])
    if len(args) > 2 and (args[1] == "-v" or args[1] == "--verbose"):
        verbose = True
    if len(args) > 3 and (args[2] == "-ai" or args[2] == "--ai"):
        with_ai = True
    if len(args) > 4 and args[3].isdigit():
        time_for_firefights = int(args[4])
    if len(args) > 5 and args[4].isdigit():
        fire_spread_rate = float(args[5])
    if len(args) > 6 and args[5].isdigit():
        max_visibility = int(args[6])
    if len(args) > 7 and args[6].isdigit():
        min_visibility = int(args[7])
    if len(args) > 8 and args[7].isdigit():
        max_strength = int(args[8])
    if len(args) > 9 and args[8].isdigit():
        min_strength = int(args[9])
    if len(args) > 10 and args[9].isdigit():
        max_speed = int(args[10])
    if len(args) > 11 and args[10].isdigit():
        min_speed = int(args[11])
    if len(args) > 12 and args[11].isdigit():
        max_fear = int(args[12])
    if len(args) > 13 and args[12].isdigit():
        min_fear = int(args[13])
    if len(args) > 14 and args[13].isdigit():
        max_age = int(args[14])
    if len(args) > 15 and args[14].isdigit():
        min_age = int(args[15])
    if len(args) > 16 and args[15].isdigit():
        max_health = int(args[16])
    if len(args) > 17 and args[16].isdigit():
        min_health = int(args[17])
    if len(args) > 18 and args[17].isdigit():
        follower_probability = float(args[18])

    # log arguments
    logging.info(f"Number of people: {number_of_people}")
    logging.info(f"Verbose: {verbose}")
    logging.info(f"With AI: {with_ai}")
    logging.info(f"Time for firefights: {time_for_firefights}")
    logging.info(f"Fire spread rate: {fire_spread_rate}")
    logging.info(f"Max visibility: {max_visibility}")
    logging.info(f"Min visibility: {min_visibility}")
    logging.info(f"Max strength: {max_strength}")
    logging.info(f"Min strength: {min_strength}")
    logging.info(f"Max speed: {max_speed}")
    logging.info(f"Min speed: {min_speed}")
    logging.info(f"Max fear: {max_fear}")
    logging.info(f"Min fear: {min_fear}")
    logging.info(f"Max age: {max_age}")
    logging.info(f"Min age: {min_age}")
    logging.info(f"Max health: {max_health}")
    logging.info(f"Min health: {min_health}")
    logging.info(f"Follower probability: {follower_probability}")

    # create simulation
    simulation = Simulation(
        number_of_people,
        n,
        time_for_firefights,
        fire_spread_rate,
        max_visibility,
        min_visibility,
        max_strength,
        min_strength,
        max_speed,
        min_speed,
        max_fear,
        min_fear,
        max_age,
        min_age,
        max_health,
        min_health,
        follower_probability,
        verbose,
        with_ai
    )
    # see statistics before evacuation
    simulation.statistics()
    # evacuate the building
    simulation.evacuate()
    # see statistics after evacuation
    simulation.statistics()


if __name__ == '__main__':
    main(argv[1:])
