from random import randint
from colors import person_colors


# Blue : Copycat
# Teal : Cheater
# Pink : Cooperator
# Yellow : Grudger
# Orange : Detective
# Tan : Copykitten
# Green : Simpleton
# Purple : Random

type_pk_to_type = {
    1: "Copycat",
    2: "Cheater",
    3: "Cooperator",
    4: "Grudger",
    5: "Detective",
    6: "Copykitten",
    7: "Simpleton",
    8: "Random",
}

type_to_color = {
    "Small Copycat": "Light Blue",
    "Normal Copycat": "Blue",
    "Large Copycat": "Dark Blue",
    "Small Cheater": "Light Teal",
    "Normal Cheater": "Teal",
    "Large Cheater": "Dark Teal",
    "Small Cooperator": "Light Pink",
    "Normal Cooperator": "Pink",
    "Large Cooperator": "Dark Pink",
    "Small Grudger": "Light Yellow",
    "Normal Grudger": "Yellow",
    "Large Grudger": "Dark Yellow",
    "Small Detective": "Light Orange",
    "Normal Detective": "Orange",
    "Large Detective": "Dark Orange",
    "Small Copykitten": "Light Tan",
    "Normal Copykitten": "Tan",
    "Large Copykitten": "Dark Tan",
    "Small Simpleton": "Light Green",
    "Normal Simpleton": "Green",
    "Large Simpleton": "Dark Green",
    "Small Random": "Light Purple",
    "Normal Random": "Purple",
    "Large Random": "Dark Purple",
}

color_to_type = {
    "Light Blue": "Small Copycat",
    "Blue": "Normal Copycat",
    "Dark Blue": "Large Copycat",
    "Light Teal": "Small Cheater",
    "Teal": "Normal Cheater",
    "Dark Teal": "Large Cheater",
    "Light Pink": "Small Cooperator",
    "Pink": "Normal Cooperator",
    "Dark Pink": "Large Cooperator",
    "Light Yellow": "Small Grudger",
    "Yellow": "Normal Grudger",
    "Dark Yellow": "Large Grudger",
    "Light Orange": "Small Detective",
    "Orange": "Normal Detective",
    "Dark Orange": "Large Detective",
    "Light Tan": "Small Copykitten",
    "Tan": "Normal Copykitten",
    "Dark Tan": "Large Copykitten",
    "Light Green": "Small Simpleton",
    "Green": "Normal Simpleton",
    "Dark Green": "Large Simpleton",
    "Light Purple": "Small Random",
    "Purple": "Normal Random",
    "Dark Purple": "Large Random",
}


class Person:
    def __init__(self, name, pk, location):

        self.name = name
        self.pk = pk
        self.age = randint(10, 61)
        # this effects how the person will do in a fight
        self.strength = randint(1, 4)
        # how many blocks can the person move in one turn
        self.speed = randint(1, 4)
        # how many blocks can the person see
        self.vision = randint(1, 11)
        # how many blocks can the person remember
        self.familiarity = randint(1, 11)
        # how likely the person is to panic
        self.fear = randint(1, 11)
        # where the person is located
        self.location = location
        # how many turns the person has been lost
        self.lost_counter = 0
        # how many turns the person has won
        self.won_counter = 0
        # how much health the person has if the person's health reaches 0, the person dies
        self.health = 100

        self.type_pk = randint(1, 8)
        if self.strength > 3:
            extra = "Large"
        elif self.strength > 2:
            extra = "Normal"
        else:
            extra = "Small"
        self.type = f"{extra} " + type_pk_to_type[self.type_pk]
        self.color_title = type_to_color[self.type]
        self.color = person_colors[self.color_title]
        if self.fear > 5:
            self.strategy = "defect"
        else:
            self.strategy = "cooperate"

    def switch_strategy(self):
        if self.strategy == "defect":
            self.strategy = "cooperate"
        else:
            self.strategy = "defect"
