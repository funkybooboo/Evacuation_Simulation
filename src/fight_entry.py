class FightEntry:
    def __init__(self, my_pk, opponent_pk, fight_time, my_strategy, opponent_strategy):
        self.my_pk = my_pk
        self.opponent_pk = opponent_pk
        self.fight_time = fight_time
        self.my_strategy = my_strategy
        self.opponent_strategy = opponent_strategy

    def __str__(self):
        return f'{self.my_pk} fought {self.opponent_pk} at {self.fight_time} mine {self.my_strategy} theirs {self.opponent_strategy}'
