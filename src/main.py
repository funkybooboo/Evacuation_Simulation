from simulation.simulation import Simulation
from os import mkdir
import logging
import argparse


def main(args):
    # create log directory
    with open('simulation/run', 'r') as f:
        simulation_count = int(f.read())
    with open('simulation/run', 'w') as f:
        f.write(str(simulation_count + 1))
    mkdir(f'../logs/run{simulation_count}')

    # set up logging
    logging.basicConfig(filename=f'../logs/run{simulation_count}/main.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    personalities = {
        "copycat": args.copycat,
        "cooperator": args.cooperator,
        "detective": args.detective,
        "simpleton": args.simpleton,
        "cheater": args.cheater,
        "grudger": args.grudger,
        "copykitten": args.copykitten,
        "random": args.random
    }

    # log arguments
    logging.info(f"Number of people: {args.number_of_people}")
    logging.info(f"Verbose: {args.verbose}")
    logging.info(f"With AI: {args.with_ai}")
    logging.info(f"Time for firefighters: {args.time_for_firefighters}")
    logging.info(f"Fire spread rate: {args.fire_spread_rate}")
    logging.info(f"Max visibility: {args.max_visibility}")
    logging.info(f"Min visibility: {args.min_visibility}")
    logging.info(f"Max strength: {args.max_strength}")
    logging.info(f"Min strength: {args.min_strength}")
    logging.info(f"Max speed: {args.max_speed}")
    logging.info(f"Min speed: {args.min_speed}")
    logging.info(f"Max fear: {args.max_fear}")
    logging.info(f"Min fear: {args.min_fear}")
    logging.info(f"Max age: {args.max_age}")
    logging.info(f"Min age: {args.min_age}")
    logging.info(f"Max health: {args.max_health}")
    logging.info(f"Min health: {args.min_health}")
    logging.info(f"Follower probability: {args.follower_probability}")
    logging.info(f"Familiarity: {args.familiarity}")
    logging.info(f"Personalities: {personalities}")

    if args.verbose:
        print(f"Number of people: {args.number_of_people}")
        print(f"Verbose: {args.verbose}")
        print(f"With AI: {args.with_ai}")
        print(f"Time for firefighters: {args.time_for_firefighters}")
        print(f"Fire spread rate: {args.fire_spread_rate}")
        print(f"Max visibility: {args.max_visibility}")
        print(f"Min visibility: {args.min_visibility}")
        print(f"Max strength: {args.max_strength}")
        print(f"Min strength: {args.min_strength}")
        print(f"Max speed: {args.max_speed}")
        print(f"Min speed: {args.min_speed}")
        print(f"Max fear: {args.max_fear}")
        print(f"Min fear: {args.min_fear}")
        print(f"Max age: {args.max_age}")
        print(f"Min age: {args.min_age}")
        print(f"Max health: {args.max_health}")
        print(f"Min health: {args.min_health}")
        print(f"Follower probability: {args.follower_probability}")
        print(f"Familiarity: {args.familiarity}")
        print(f"Personalities: {personalities}")

    # create simulation
    simulation = Simulation(
        args.number_of_people,
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
        args.follower_probability,
        args.verbose,
        args.with_ai,
        args.familiarity,
        personalities
    )
    # see statistics before evacuation
    simulation.statistics()
    # evacuate the building
    simulation.evacuate()
    # see statistics after evacuation
    simulation.statistics()


def get_args():
    parser = argparse.ArgumentParser(description='Evacuation Simulation')
    # Add arguments
    parser.add_argument('--number_of_people', type=int, help='Number of people', default=50)
    parser.add_argument('--verbose', type=bool, help='Verbosity', default=False)
    parser.add_argument('--with_ai', type=bool, help='With AI', default=False)
    parser.add_argument('--time_for_firefighters', type=int, help='Time for firefighters', default=1000)
    parser.add_argument('--fire_spread_rate', type=int, help='Fire spread rate', default=0.1)
    parser.add_argument('--max_visibility', type=int, help='Maximum visibility', default=5)
    parser.add_argument('--min_visibility', type=int, help='Minimum visibility', default=1)
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
    parser.add_argument('--follower_probability', type=float, help='Follower probability', default=0.5)
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
    if args.follower_probability < 0 or args.follower_probability > 1:
        raise ValueError("Follower probability must be between 0 and 1")
    if args.familiarity < 0:
        raise ValueError("Familiarity must be greater than 0")
    if args.copycat + args.cooperator + args.detective + args.simpleton + args.cheater + args.grudger + args.copykitten + args.random != 1:
        raise ValueError("Sum of all personalities must be 1")


if __name__ == "__main__":
    main(get_args())
