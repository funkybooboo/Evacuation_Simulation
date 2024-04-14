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
        self.strategy_history = []

    @abstractmethod
    def get_strategy(self, opponent_strategy, fight_history) -> Strategy:
        pass


class Copycat(Personality):
    def get_strategy(self, opponent_strategy):
        if not opponent_strategy:
            return Strategy.cooperate
        if opponent_strategy == Strategy.cooperate:
            return Strategy.cooperate
        else:
            return Strategy.defect


class Cooperator(Personality):
    def get_strategy(self, opponent_strategy):
        return Strategy.cooperate


class Detective(Personality): 
    # Starts with: Cooperate, Defect, Cooperate, Cooperate. 
    # Afterwards, if your opponent ever retaliates with a Defect, it plays like a Copycat. 
    # Otherwise, it plays like an Always Defect.
    def get_strategy(self, opponent_strategy, fight_history):
        if len(self.strategy_history) == 0:
            self.strategy_history.append(Strategy.cooperate)
            return Strategy.cooperate
        if len(self.strategy_history) == 1:
            self.strategy_history.append(Strategy.defect)
            return Strategy.defect
        if len(self.strategy_history) == 2 or len(self.strategy_history) == 3:
            self.strategy_history.append(Strategy.cooperate)
            return Strategy.cooperate
        if not opponent_strategy:
            self.strategy_history = []
            return self.get_strategy(opponent_strategy)
        if opponent_strategy == Strategy.defect:
            if self.opponent_strategy == Strategy.cooperate:
                return Strategy.cooperate
            return Strategy.defect
        return Strategy.defect


class Simpleton(Personality):
    """
    cooperates when you cooperate with it, except by mistake
    “pushes boundaries” and keeps defecting when you cooperate, until you retaliate
    “concedes when punished” and cooperates after a defect/defect result
    “retaliates against unprovoked aggression”, defecting if you defect on it while it cooperates.
    """
    def get_strategy(self, opponent_strategy):
        if not opponent_strategy:
            return Strategy.cooperate
        if opponent_strategy == Strategy.cooperate:
            return Strategy.cooperate
        if opponent_strategy == Strategy.defect and self.strategy_history == Strategy.cooperate:
            return Strategy.defect
        if opponent_strategy == Strategy.defect and self.strategy_history == Strategy.defect:
            return Strategy.cooperate


class Cheater(Personality):
    def get_strategy(self, opponent_strategy):
        return Strategy.defect


class Grudger(Personality):
    def get_strategy(self, opponent_strategy):
        pass


class Copykitten(Personality):
    def get_strategy(self, opponent_strategy):
        pass


class Random(Personality):
    def get_strategy(self, opponent_strategy):
        return Strategy.cooperate if randint(0, 1) == 1 else Strategy.defect
