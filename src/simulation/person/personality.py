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
    def get_strategy(self, opponent_strategy, fight_history):
        if not opponent_strategy:
            return Strategy.cooperate
        if opponent_strategy == Strategy.cooperate:
            return Strategy.cooperate
        else:
            return Strategy.defect


class Cooperator(Personality):
    def get_strategy(self, opponent_strategy, fight_history):
        return Strategy.cooperate


class Detective(Personality): 
    # Starts with: Cooperate, Defect, Cooperate, Cooperate. 
    # Afterward, if your opponent ever retaliates with a Defect, it plays like a Copycat.
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
            return self.get_strategy(opponent_strategy, fight_history)
        if opponent_strategy == Strategy.defect:
            if opponent_strategy == Strategy.cooperate:
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
    def get_strategy(self, opponent_strategy, fight_history):
        if not opponent_strategy:
            return Strategy.cooperate
        if len(fight_history)-1 == -1:
            return Strategy.cooperate
        if len(fight_history)-1 == 0:
            return Strategy.cooperate
        if len(fight_history)-1 == 1 and opponent_strategy == Strategy.defect:
            return Strategy.defect
        if len(fight_history)-1 == 1 and opponent_strategy == Strategy.cooperate:
            return Strategy.cooperate
        if len(fight_history)-1 > 1 and opponent_strategy == Strategy.defect:
            return Strategy.defect
        if len(fight_history)-1 > 1 and opponent_strategy == Strategy.cooperate:
            return Strategy.cooperate


class Cheater(Personality):
    def get_strategy(self, opponent_strategy, fight_history):
        return Strategy.defect


class Grudger(Personality):
    """
    Starts with cooperate and continues cooperating until you defect even once.
    From then on it will always defect no matter what you do.
    """
    def get_strategy(self, opponent_strategy, fight_history):
        has_defected = False
        for fight_entry in fight_history:
            if fight_entry.opponent_strategy == Strategy.defect:
                has_defected = True
                break
        if has_defected:
            return Strategy.defect
        return Strategy.cooperate


class Copykitten(Personality):
    def get_strategy(self, opponent_strategy, fight_history):
        if opponent_strategy == Strategy.cooperate:
            return Strategy.cooperate
        last_strategy = fight_history[len(fight_history)-1]
        last_last_strategy = fight_history[len(fight_history)-2]
        if last_strategy == Strategy.cooperate or last_last_strategy == Strategy.cooperate:
            return Strategy.cooperate
        return Strategy.defect


class Random(Personality):
    def get_strategy(self, opponent_strategy, fight_history):
        return Strategy.cooperate if randint(0, 1) == 1 else Strategy.defect
