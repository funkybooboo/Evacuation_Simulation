from random import randint
from abc import ABC, abstractmethod
from .strategy import Strategy


class Personality(ABC):
    def __init__(self):
        self.strategy_history = []

    @abstractmethod
    def get_strategy(self, opponent_strategy, fight_history) -> Strategy:
        pass


class Copycat(Personality):
    def get_strategy(self, opponent_strategy, fight_history):
        if not opponent_strategy:
            return Strategy.cooperate
        return opponent_strategy


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
        has_defected = False
        for fight_entry in fight_history:
            if fight_entry.opponent_strategy == Strategy.defect:
                has_defected = True
                break
        if has_defected:
            if not opponent_strategy:
                return Strategy.cooperate
            return opponent_strategy
        return Strategy.defect


class Simpleton(Personality):
    """
    if opponent cooperates, it will cooperate unless opponent defect twice in a row
    if opponent cooperates, then defect, it will cooperate
    if opponent defect, and it defected, it will cooperate
    """
    def get_strategy(self, opponent_strategy, fight_history):
        if len(fight_history) == 0:
            if opponent_strategy:
                if opponent_strategy == Strategy.cooperate:
                    return Strategy.cooperate
                return Strategy.defect
            return Strategy.cooperate
        else:
            if opponent_strategy:
                last_strategy = opponent_strategy
                last_last_strategy = fight_history[len(fight_history)-1].opponent_strategy
            else:
                if len(fight_history) > 1:
                    last_strategy = fight_history[len(fight_history)-1].opponent_strategy
                    last_last_strategy = fight_history[len(fight_history)-2].opponent_strategy
                else:
                    return Strategy.cooperate
            if last_strategy == Strategy.defect and last_last_strategy == Strategy.defect:
                return Strategy.defect
            if last_strategy == Strategy.defect and last_last_strategy == Strategy.cooperate:
                return Strategy.cooperate
            if last_strategy == Strategy.defect and last_last_strategy == Strategy.defect:
                return Strategy.cooperate
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
        if len(fight_history) == 0:
            return Strategy.cooperate
        if opponent_strategy:
            last_strategy = opponent_strategy
            last_last_strategy = fight_history[len(fight_history)-1].opponent_strategy
        else:
            if len(fight_history) > 1:
                last_strategy = fight_history[len(fight_history) - 1].opponent_strategy
                last_last_strategy = fight_history[len(fight_history)-2].opponent_strategy
            else:
                return Strategy.cooperate
        if last_strategy == Strategy.defect and last_last_strategy == Strategy.defect:
            return Strategy.defect
        if last_strategy == Strategy.cooperate and last_last_strategy == Strategy.cooperate:
            return Strategy.cooperate
        return Strategy.cooperate


class Random(Personality):
    def get_strategy(self, opponent_strategy, fight_history):
        return Strategy.cooperate if randint(0, 1) == 1 else Strategy.defect
