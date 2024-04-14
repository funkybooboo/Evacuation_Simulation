from random import randint
from openai import OpenAI
from dotenv import load_dotenv
import os


class Choice:
    def __init__(self, person):
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
        self.situation = self.get_situation_string()
        self.options = self.get_options()
        self.temperature = self.get_temperature()
        self.options_with_text = self.get_options_with_text()
        self.person = person

    def make(self):
        if self.person.simulation.choice_mode == 0:
            choice = self.get_random_choice()
        elif self.person.simulation.choice_mode == 1:
            choice = self.get_choice_from_AI()
        elif self.person.simulation.choice_mode == 2:
            choice = self.get_choice_from_logic()
        elif self.person.simulation.choice_mode == 3:
            choice = self.get_choice_from_user()
        else:
            raise Exception("Invalid choice mode")
        return choice, self.make_choice(choice)

    def make_choice(self, choice):
        if choice is None:
            raise Exception("AI did not give a valid choice")
        if choice == 'A':
            return self.person.explore()
        elif choice == 'B':
            return self.person.move_randomly()
        elif choice == 'C':
            closest_person = self.person.get_closest(self.person.location, self.person.memory.people)
            return self.person.move_towards(closest_person)
        elif choice == 'D':
            closest_door = self.person.get_closest(self.person.location, self.person.memory.doors)
            return self.person.move_towards(closest_door)
        elif choice == 'E':
            closest_glass = self.person.get_closest(self.person.location, self.person.memory.glasses)
            return self.person.move_towards(closest_glass)
        elif choice == 'F':
            closest_fire = self.person.get_closest(self.person.location, self.person.memory.fires)
            return self.person.move_towards(closest_fire)
        elif choice == 'G':
            closest_glass = self.person.get_closest(self.person.location, self.person.memory.glasses)
            if not self.person.break_glass(closest_glass):
                raise Exception("Cant break glass unless you are near it")
            return None
        elif choice == 'H':
            closest_person = self.person.get_closest(self.person.location, self.person.memory.people)
            return self.person.move_towards(closest_person)
        elif choice == 'I':
            closest_door = self.person.get_closest(self.person.location, self.person.memory.doors)
            return self.person.move_towards(closest_door)
        elif choice == 'J':
            closest_glass = self.person.get_closest(self.person.location, self.person.memory.broken_glass)
            return self.person.jump_out_of_window(closest_glass)
        elif choice == 'K':
            return self.person.follow_evacuation_plan()
        elif choice == 'L':
            closest_exit = self.person.get_closest(self.person.location, self.person.memory.exits)
            return self.person.move_towards(closest_exit)
        elif choice == 'M':
            closest_stair = self.person.get_closest(self.person.location, self.person.memory.stairs)
            return self.person.move_towards(closest_stair)
        elif choice == 'N':
            return None
        else:
            raise Exception("Invalid choice")

    def get_temperature(self):
        if self.person.fear >= 5:
            return 0.7
        else:
            return 0.3

    def get_situation_string(self):
        situation = \
            f"""
            Do you like people: {self.person.is_follower}
            Floor: {self.person.location[0]}
            Strength: {self.person.strength}
            Health: {self.person.health}
            Age: {self.person.age}
            Fear: {self.person.fear}
            Nearest Exit: {self.person.get_closest(self.person.location, self.person.memory.exits)}
            Nearest Stairs: {self.person.get_closest(self.person.location, self.person.memory.stairs)}
            Nearest Person: {self.person.get_closest(self.person.location, self.person.memory.people)}
            Nearest Window: {self.person.get_closest(self.person.location, self.person.memory.glasses)}
            Nearest Door: {self.person.get_closest(self.person.location, self.person.memory.doors)}
            Nearest Fire: {self.person.get_closest(self.person.location, self.person.memory.fires)}
            People Near: {self.person.get_number_of_people_near()}
            Know Evacuation Plan: {self.person.memory.exit_plans}
            Time to Get Out: {self.person.get_time_to_get_out()}
            Room Type: {self.person.room_type}
            """
        return situation

    def get_options(self):
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

    def get_response_from_AI(self):
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

    def get_random_choice(self):
        return self.options[randint(0, len(self.options) - 1)]

    def get_choice_from_AI(self):
        response = self.get_response_from_AI()
        if response is None:
            return None
        if response in self.options:
            return response
        else:
            return None

    def get_options_with_text(self):
        options_with_text = ""
        for option in self.options:
            options_with_text += option
            options_with_text += ": "
            options_with_text += self.text[option]
            options_with_text += "\n"
        return options_with_text

    def get_choice_from_logic(self):
        pass

    def get_choice_from_user(self):
        pass
