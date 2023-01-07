from kravy import Player, Card
import random


class RandomPlayer(Player):
    """
    A player that always select a random card to play.
    """

    def __init__(self, name:str, take_min=False):
        super().__init__(name)
        self.take_min = take_min

    def select_card(self, hand: list[Card], rows: list[list[Card]]) -> Card:
        i = random.randint(0, len(hand)-1)
        return hand[i]

    def select_row(self, rows: list[list[Card]]) -> int:
        if self.take_min:
            min_p = float("inf")
            min_i = 0
            for i, row in enumerate(rows):
                p = sum([c.points for c in row])
                if p < min_p:
                    min_p = p
                    min_i = i
            return min_i
        else:
            return random.randint(0, len(rows)-1)

