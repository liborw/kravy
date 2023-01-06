
from dataclasses import dataclass

@dataclass
class Card:
    value: int
    points: int

    def __repr__(self) -> str:
        return f"{self.value}|{self.points}"

Cards = list[Card]

def default_deck() -> Cards:
    deck = list()
    for i in range(1, 105):
        if i == 55:
            card = Card(i, 7)
        elif i % 11 == 0:
            card = Card(i, 5)
        elif i % 10 == 0:
            card = Card(i, 3)
        elif i % 5 == 0:
            card = Card(i, 2)
        else:
            card = Card(i, 1)
        deck.append(card)
    return deck

print(default_deck())


#%%

@dataclass
class GameState():
    step: int
    rows: list[Cards]

    def __repr__(self) -> str:
        return f"{self.step}: {self.rows}"





class Game():

    def __init__(self, args):
        pass




