from simulation.simulation import Simulation
from os import mkdir
from src.simulation.logger import setup_logger
import argparse


def main(args):
    # create log directory
    with open('simulation/run', 'r') as f:
        simulation_count = int(f.read())
    with open('simulation/run', 'w') as f:
        f.write(str(simulation_count + 1))
    mkdir(f'../logs/run{simulation_count}')
    mkdir(f'../logs/run{simulation_count}/people')
    mkdir(f'../logs/run{simulation_count}/simulation')

    # set up logging
    logger = setup_logger("main_logger", f'../logs/run{simulation_count}/main.log', args.verbose)
    logger.info('This log is for INFO purposes from main')

    personalities = {
        "Copycat": args.copycat,
        "Cooperator": args.cooperator,
        "Detective": args.detective,
        "Simpleton": args.simpleton,
        "Cheater": args.cheater,
        "Grudger": args.grudger,
        "Copykitten": args.copykitten,
        "Random": args.random
    }

    # log arguments
    logger.info(f"Time to view images: {args.time_to_view_images}")
    logger.info(f"Number of people: {args.number_of_people}")
    logger.info(f"Number of floors: {args.number_of_floors}")
    logger.info(f"Verbose: {args.verbose}")
    logger.info(f"Choice Mode: {args.choice_mode}")
    logger.info(f"Time for firefighters: {args.time_for_firefighters}")
    logger.info(f"Fire spread rate: {args.fire_spread_rate}")
    logger.info(f"Max visibility: {args.max_visibility}")
    logger.info(f"Min visibility: {args.min_visibility}")
    logger.info(f"Max strength: {args.max_strength}")
    logger.info(f"Min strength: {args.min_strength}")
    logger.info(f"Max speed: {args.max_speed}")
    logger.info(f"Min speed: {args.min_speed}")
    logger.info(f"Max fear: {args.max_fear}")
    logger.info(f"Min fear: {args.min_fear}")
    logger.info(f"Max age: {args.max_age}")
    logger.info(f"Min age: {args.min_age}")
    logger.info(f"Max health: {args.max_health}")
    logger.info(f"Min health: {args.min_health}")
    logger.info(f"Likes people probability: {args.likes_people_probability}")
    logger.info(f"Familiarity: {args.familiarity}")
    logger.info(f"Personalities: {personalities}")

    logger.info("creating simulation")
    # create simulation
    simulation = Simulation(
        args.time_to_view_images,
        args.number_of_people,
        args.number_of_floors,
        simulation_count,
        args.time_for_firefighters,
        args.fire_spread_rate,
        args.max_visibility,
        args.min_visibility,
        args.max_strength,
        args.min_strength,
        args.max_speed,
        args.min_speed,
        args.max_fear,
        args.min_fear,
        args.max_age,
        args.min_age,
        args.max_health,
        args.min_health,
        args.likes_people_probability,
        args.verbose,
        args.choice_mode,
        args.familiarity,
        personalities
    )
    # see statistics before evacuation
    simulation.statistics()
    logger.info("evacuating")
    # evacuate the building
    simulation.evacuate()
    # see statistics after evacuation
    simulation.statistics()


def get_args():
    parser = argparse.ArgumentParser(description='Evacuation Simulation')
    # Add arguments
    parser.add_argument("--time_to_view_images", type=int, help="Time to view images", default=0)
    parser.add_argument('--number_of_people', type=int, help='Number of people', default=50)
    parser.add_argument('--number_of_floors', type=int, help='Number of floors. 1-3', default=3)
    parser.add_argument('--verbose', type=bool, help='Verbosity', default=False)
    parser.add_argument('--choice_mode', type=int, help='How do people make choices? 0: Random, 1: AI, 2: Logic, 3: You Choose!', default=2)
    parser.add_argument('--time_for_firefighters', type=int, help='Time for firefighters', default=50)
    parser.add_argument('--fire_spread_rate', type=int, help='Fire spread rate', default=0.05)
    parser.add_argument('--max_visibility', type=int, help='Maximum visibility', default=20)
    parser.add_argument('--min_visibility', type=int, help='Minimum visibility', default=15)
    parser.add_argument('--max_strength', type=int, help='Maximum strength', default=10)
    parser.add_argument('--min_strength', type=int, help='Minimum strength', default=1)
    parser.add_argument('--max_speed', type=int, help='Maximum speed', default=5)
    parser.add_argument('--min_speed', type=int, help='Minimum speed', default=1)
    parser.add_argument('--max_fear', type=int, help='Maximum fear', default=10)
    parser.add_argument('--min_fear', type=int, help='Minimum fear', default=1)
    parser.add_argument('--max_age', type=int, help='Maximum age', default=80)
    parser.add_argument('--min_age', type=int, help='Minimum age', default=18)
    parser.add_argument('--max_health', type=int, help='Maximum health', default=100)
    parser.add_argument('--min_health', type=int, help='Minimum health', default=80)
    parser.add_argument('--likes_people_probability', type=float, help='Likes people probability', default=0.75)
    parser.add_argument('--familiarity', type=int, help='Familiarity', default=10)
    parser.add_argument('--copycat', type=float, help='Copycat', default=0.125)
    parser.add_argument('--cooperator', type=float, help='Cooperator', default=0.125)
    parser.add_argument('--detective', type=float, help='Detective', default=0.125)
    parser.add_argument('--simpleton', type=float, help='Simpleton', default=0.125)
    parser.add_argument('--cheater', type=float, help='Cheater', default=0.125)
    parser.add_argument('--grudger', type=float, help='Grudger', default=0.125)
    parser.add_argument('--copykitten', type=float, help='Copykitten', default=0.125)
    parser.add_argument('--random', type=float, help='Random', default=0.125)
    # Parse arguments
    args = parser.parse_args()
    validate_args(args)
    return args


def validate_args(args):
    if not args:
        raise ValueError("No arguments provided")
    if args.time_to_view_images < 0:
        raise ValueError("Time to view images must be greater than 0")
    if args.max_visibility < args.min_visibility:
        raise ValueError("Max visibility must be greater than min visibility")
    if args.max_strength < args.min_strength:
        raise ValueError("Max strength must be greater than min strength")
    if args.max_speed < args.min_speed:
        raise ValueError("Max speed must be greater than min speed")
    if args.max_fear < args.min_fear:
        raise ValueError("Max fear must be greater than min fear")
    if args.max_age < args.min_age:
        raise ValueError("Max age must be greater than min age")
    if args.max_health < args.min_health:
        raise ValueError("Max health must be greater than min health")
    if args.likes_people_probability < 0 or args.likes_people_probability > 1:
        raise ValueError("Follower probability must be between 0 and 1")
    if args.familiarity < 0:
        raise ValueError("Familiarity must be greater than 0")
    if args.copycat + args.cooperator + args.detective + args.simpleton + args.cheater + args.grudger + args.copykitten + args.random != 1:
        raise ValueError("Sum of all personalities must be 1")
    if args.choice_mode < 0 or args.choice_mode > 3:
        raise ValueError("Choice mode must be 0, 1, 2, or 3")
    if args.number_of_floors < 1 or args.number_of_floors > 3:
        raise ValueError("Number of floors must be between 1 and 3")


if __name__ == "__main__":
    main(get_args())
