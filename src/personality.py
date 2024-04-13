from random import randint
from abc import ABC, abstractmethod
from strategy import Strategy


class Personality(ABC):
    def __init__(self):
        self.fight_count = 0
        self.win_count = 0
        self.draw_count = 0
        self.lose_count = 0
        self.loose_in_a_row = 0
        self.win_in_a_row = 0
        self.draw_in_a_row = 0
        self.last_strategy = None
        self.strategy = Strategy.cooperate if randint(0, 1) == 0 else Strategy.defect

    def switch_strategy(self):
        self.last_strategy = self.strategy
        if self.strategy == Strategy.defect:
            self.strategy = Strategy.cooperate
        else:
            self.strategy = Strategy.defect

    @abstractmethod
    def get_strategy(self):
        pass


class Copycat(Personality):
    def get_strategy(self):
        pass


class Cooperator(Personality):
    def get_strategy(self):
        pass


class Detective(Personality):
    def get_strategy(self):
        pass


class Simpleton(Personality):
    def get_strategy(self):
        pass


class Cheater(Personality):
    def get_strategy(self):
        pass


class Grudger(Personality):
    def get_strategy(self):
        pass


class Copykitten(Personality):
    def get_strategy(self):
        pass


class Random(Personality):
    def get_strategy(self):
        pass
