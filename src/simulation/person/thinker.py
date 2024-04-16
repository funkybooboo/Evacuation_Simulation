from random import randint
from openai import OpenAI
from dotenv import load_dotenv
import os
from src.simulation.logger import setup_logger


class Thinker:
    def __init__(self, person):
        self.logger = setup_logger("choice_logger", f'../logs/run{person.simulation.simulation_count}/people/person{person.pk}/choice.log', person.simulation.verbose)

        self.text = {
            "A": "Explore",
            "B": "Move randomly",
            "C": "Move towards a person",
            "D": "Move towards a door",
            "E": "Move towards window",
            "F": "Move towards the fire",
            "G": "Break window",
            "H": "Fight someone for a spot",
            "I": "Run through fire to safety",
            "J": "Jump out of building",
            "K": "Follow evacuation plan",
            "L": "Move to exit",
            "M": "Move to stair",
            "N": "Do nothing"
        }
        self.valid = self.text.keys()
        self.situation = ""
        self.options = ""
        self.temperature = 0
        self.options_with_text = ""
        self.person = person

    def think(self):
        self.__refresh_info()
        if self.person.simulation.choice_mode == 0:
            choice = self.__get_random_choice()
        elif self.person.simulation.choice_mode == 1:
            choice = self.__get_choice_from_AI()
        elif self.person.simulation.choice_mode == 2:
            choice = self.__get_choice_from_logic()
        elif self.person.simulation.choice_mode == 3:
            choice = self.__get_choice_from_user()
        else:
            raise Exception("Invalid choice mode")
        self.logger.info(f"Choice: {choice}")
        return self.__make(choice)

    def __refresh_info(self):
        self.situation = self.__get_situation_string()
        self.options = self.__get_options()
        self.temperature = self.__get_temperature()
        self.options_with_text = self.__get_options_with_text()
        self.logger.info(f"Situation: {self.situation}")
        self.logger.info(f"Options: {self.options}")
        self.logger.info(f"Temperature: {self.temperature}")

    def __make(self, choice):
        if choice is None:
            raise Exception("AI did not give a valid choice")
        if choice == 'A':
            return self.person.movement.explore()
        elif choice == 'B':
            return self.person.movement.randomly()
        elif choice == 'C':
            closest_person = self.person.movement.get_closest(self.person.location, self.person.memory.people)
            return self.person.movement.towards(closest_person)
        elif choice == 'D':
            closest_door = self.person.movement.get_closest(self.person.location, self.person.memory.doors)
            return self.person.movement.towards(closest_door)
        elif choice == 'E':
            closest_glass = self.person.movement.get_closest(self.person.location, self.person.memory.glasses)
            return self.person.movement.towards(closest_glass)
        elif choice == 'F':
            closest_fire = self.person.movement.get_closest(self.person.location, self.person.memory.fires)
            return self.person.movement.towards(closest_fire)
        elif choice == 'G':
            closest_glass = self.person.movement.get_closest(self.person.location, self.person.memory.glasses)
            if not self.person.movement.break_glass(closest_glass):
                raise Exception("Cant break glass unless you are near it")
            return None
        elif choice == 'H':
            closest_person = self.person.movement.get_closest(self.person.location, self.person.memory.people)
            return self.person.movement.towards(closest_person)
        elif choice == 'I':
            closest_door = self.person.movement.get_closest(self.person.location, self.person.memory.doors)
            return self.person.movement.towards(closest_door)
        elif choice == 'J':
            broken_glass = self.person.movement.get_closest(self.person.location, self.person.memory.broken_glass)
            return self.person.movement.place(broken_glass)
        elif choice == 'K':
            return self.person.movement.follow_evacuation_plan()
        elif choice == 'L':
            closest_exit = self.person.movement.get_closest(self.person.location, self.person.memory.exits)
            return self.person.movement.towards(closest_exit)
        elif choice == 'M':
            closest_stair = self.person.movement.get_closest(self.person.location, self.person.memory.stairs)
            return self.person.movement.towards(closest_stair)
        elif choice == 'N':
            return None
        else:
            raise Exception("Invalid choice")

    def __get_temperature(self):
        if self.person.fear >= 5:
            return 0.7
        else:
            return 0.3

    def __is_irrational(self):
        return self.temperature < 0.5 and self.person.fear > 8

    def __get_situation_string(self):
        situation = \
            f"""
            Do you like people: {self.person.is_follower}
            Floor: {self.person.location[0]}
            Strength: {self.person.strength}
            Health: {self.person.health}
            Age: {self.person.age}
            Fear: {self.person.fear}
            Nearest Exit: {self.person.movement.get_closest(self.person.location, self.person.memory.exits)}
            Nearest Stairs: {self.person.movement.get_closest(self.person.location, self.person.memory.stairs)}
            Nearest Person: {self.person.movement.get_closest(self.person.location, self.person.memory.people)}
            Nearest Window: {self.person.movement.get_closest(self.person.location, self.person.memory.glasses)}
            Nearest Door: {self.person.movement.get_closest(self.person.location, self.person.memory.doors)}
            Nearest Fire: {self.person.movement.get_closest(self.person.location, self.person.memory.fires)}
            People Near: {self.person.get_number_of_people_near()}
            Know Evacuation Plan: {self.person.memory.exit_plans}
            Time to Get Out: {self.person.movement.get_time_to_get_out()}
            Room Type: {self.person.room_type}
            """
        return situation

    def __get_options(self):
        options = ["A", "B", "N"]
        if self.person.memory.exits:
            options.append("L")
        if self.person.memory.stairs:
            options.append("M")
        if self.person.memory.people:
            options.append("C")
            if self.person.is_next_to(self.person.memory.people):
                options.append("H")
        if self.person.memory.doors:
            options.append("D")
        if self.person.memory.glasses:
            options.append("E")
            if self.person.can_break_glass() and self.person.is_next_to(self.person.memory.glasses):
                options.append("G")
        if self.person.memory.fires:
            options.append("F")
        if self.person.memory.broken_glasses and self.person.is_next_to(self.person.memory.broken_glasses):
            options.append("J")
        if self.person.memory.exit_plans:
            options.append("K")
        if self.person.is_next_to(self.person.memory.fires):
            options.append("I")
        options.sort()
        return options

    def __get_response_from_AI(self):
        context = ""
        with open("../../../data/context.txt", "r") as file:
            for line in file.readlines():
                context += line
                context += "\n"

        example = ""
        with open("../../../data/example.txt", "r") as file:
            for line in file.readlines():
                example += line
                example += "\n"
        question = "Options:\n" + self.options_with_text + "\n----------------------\nPick a letter:"

        with open("../data/openai_key.txt", "r") as file:
            OPENAI_API_KEY = file.readline().strip()
        if OPENAI_API_KEY is None:
            raise Exception("couldn't get key")
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        load_dotenv()
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",  # may change model
            temperature=self.temperature,  # will be passed in fear level
            max_tokens=3000,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": context},  # Will be prompt context
                {"role": "user", "content": self.situation},  # prompt of the user
                {"role": "assistant", "content": example},  # example of response
                {"role": "user", "content": question},  # form of question or command
            ]
        )
        return response

    def __get_choice_from_AI(self):
        response = self.__get_response_from_AI()
        if response is None:
            raise Exception("AI did not respond")
        choice = self.__get_choice_from_response(response)
        if choice is None:
            raise Exception("AI did not give a valid choice")
        if choice in self.options:
            return response
        raise Exception("AI did not give a valid choice")

    @staticmethod
    def __get_choice_from_response(response):
        for message in response["choices"]:
            if message["role"] == "assistant":
                return message["content"]
        return None

    def __get_random_choice(self):
        return self.options[randint(0, len(self.options) - 1)]

    def __get_options_with_text(self):
        options_with_text = ""
        for option in self.options:
            options_with_text += option
            options_with_text += ": "
            options_with_text += self.text[option]
            options_with_text += "\n"
        return options_with_text

    def __get_choice_from_user(self):
        options_with_text = self.__get_options_with_text()
        print(f"situation: {self.situation}")
        print(f"temperature (0-1 how rational the choice should be): \n{self.temperature}")
        print(f"options_with_text: \n{options_with_text}")
        while True:
            choice = input("Please choose an option: ")
            if choice in self.options:
                return choice
            print("That's not a valid option")

    def __get_choice_from_logic(self):
        if self.__is_irrational():
            return self.__get_irrational_choice()
        else:
            return self.__get_rational_choice()

    def __get_rational_choice(self):
        if self.person.is_trapped():
            return self.__get_rational_trapped_choice()
        else:
            return self.__get_rational_untrapped_choice()

    def __get_rational_trapped_choice(self):
        if self.person.is_trapped_by_people():
            if self.person.fire_nearby():
                if self.person.can_get_to_window() and self.person.can_break_glass():
                    return "E"
                if self.person.can_get_to_broken_glass():
                    return "J"
                return "H"
            else:
                return "N"
        if self.person.is_trapped_by_fire():
            if self.person.can_get_to_window():
                return "E"
            else:
                return "I"
        return "N"

    def __get_rational_untrapped_choice(self):
        if self.person.know_about_important_location():
            if self.person.get_closest(self.person.location, self.person.memory.exits):
                return "L"
            if self.person.get_closest(self.person.location, self.person.memory.stairs):
                return "M"
            if self.person.get_closest(self.person.location, self.person.memory.exit_plans):
                return "K"
        if self.person.is_in_room():
            return "D"
        if self.person.is_in_hall():
            if self.person.get_closest(self.person.location, self.person.memory.people):
                return "C"
        return "A"

    def __get_irrational_choice(self):
        if self.person.is_trapped():
            return self.__get_irrational_trapped_choice()
        else:
            return self.__get_irrational_untrapped_choice()

    def __get_irrational_trapped_choice(self):
        if self.person.is_trapped_by_people():
            if self.person.fire_nearby():
                if self.person.can_get_to_window():
                    return "E"
                else:
                    return "H"
            else:
                return "N"
        if self.person.is_trapped_by_fire():
            if self.person.can_get_to_window():
                return "E"
            else:
                return "I"
        return "N"

    def __get_irrational_untrapped_choice(self):
        return self.__get_random_choice()