
from dataclasses import dataclass, field
import logging

@dataclass(eq=True, order=True)
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

#%%

import random

class Player():

    def __init__(self, name: str):
        self.name: str = name

    def select_card(self, hand: list[Card], state: list[list[Card]]) -> Card:
        pass

    def select_row(self, state: list[list[Card]]) -> int:
        pass


class RandomPlayer(Player):

    def __init__(self, name:str):
        super().__init__(name)

    def select_card(self, hand: list[Card], rows: list[list[Card]]) -> Card:
        i = random.randint(0, len(hand)-1)
        return hand[i]

    def select_row(self, rows: list[list[Card]]) -> int:
        # take alway the cheapest one
        min_p = float("inf")
        min_i = -1
        for i, row in enumerate(rows):
            p = sum([c.points for c in row])
            if p < min_p:
                min_p = p
                min_i = i
        return min_i


#%%

class GameState():

    def __init__(self, cards: list[Cards]):
        self.rows = [[c] for c in cards]
        self.step = 0

    def __repr__(self) -> str:
        return f"{self.rows}"

    def lowest(self):
        min_card = self.rows[0][-1]
        for row in self.rows:
            if min_card > row[-1]:
                min_card = row[-1]
        return min_card.copy()

    def find_closest_row_idx(self, card: Card) -> int|None:
        min_d = 105
        min_i = None
        for i, row in enumerate(self.rows):
            d = card.value - row[-1].value
            if d > 0 and d < min_d:
                min_d = d
                min_i = i
        return min_i

    def place_card(self, card: Card, row_idx: int):
        self.rows[row_idx].append(ros_idx)

    def row_points(self, ros_idx: int):
        return sum([c.value for c in self.rows[row_idx]])

    def replace_row(self, card: Card, row_idx: int):
        self.rows[ros_idx] = [card]

#%%

import copy

@dataclass
class PlayerState(object):
    player: Player
    hand: list[Card] = field(default_factory=list)
    score: int = 0
    card: Card|None = None

    def __repr__(self):
        return f"{self.player.name} ({self.score}): {self.hand}"

class Game():

    def __init__(self,
                 players: list[Player],
                 deck: list[Card],
                 num_rounds: int = 10,
                 num_rows: int = 4
                 ):
        self.deck = deck
        self.num_rounds = num_rounds
        self.num_rows = num_rows

        self.players = []
        for player in players:
            self.players.append(PlayerState(player))

        self.reset()

    def reset(self):
        deck = copy.deepcopy(self.deck)
        random.shuffle(deck)

        for player in self.players:
            player.hand = deck[0:self.num_rounds]
            deck = deck[self.num_rounds:]

        self.rows = [[c] for c in deck[0:self.num_rows]]

    def lowest(self):
        min_card = self.rows[0][-1]
        for row in self.rows:
            if min_card > row[-1]:
                min_card = row[-1]
        return copy.deepcopy(min_card)

    def find_closest_row_idx(self, card: Card) -> int|None:
        min_d = 105
        min_i = None
        for i, row in enumerate(self.rows):
            d = card.value - row[-1].value
            if d > 0 and d < min_d:
                min_d = d
                min_i = i
        return min_i

    def row_points(self, row_idx: int):
        return sum([c.points for c in self.rows[row_idx]])

    def round(self):
        print(f"state: {self.rows}")

        for ps in self.players:
            ps.card = ps.player.select_card(
                    copy.deepcopy(ps.hand),
                    copy.deepcopy(self.rows)
            )

        lowest = self.lowest()
        for ps in sorted(self.players, key=lambda ps: ps.card):
            ps.hand.remove(ps.card)
            print(f"{ps.player.name} chosed {ps.card}")

            if ps.card < lowest:
                print(f"{ps.card} is lower that all rows")
                row_idx = ps.player.select_row(copy.deepcopy(self.rows))
                points = self.row_points(row_idx)
                ps.score += points
                print(f"{ps.player.name} chosed to take {row_idx} row with {points} points")
                self.rows[row_idx] = [ps.card]
                continue

            row_idx = self.find_closest_row_idx(ps.card)
            if len(self.rows[row_idx]) >= 5:
                points = self.row_points(row_idx)
                ps.score += points
                print(f"{ps.card} will go on {row_idx} and is sixth and get {points} points")
                self.rows[row_idx] = [ps.card]
                continue

            print(f"{ps.card} will go on {row_idx} and is safe")
            self.rows[row_idx].append(ps.card)




game = Game(
        [
            RandomPlayer("A"),
            RandomPlayer("B"),
            RandomPlayer("C"),
            RandomPlayer("D")
        ],
        default_deck()
)

for _ in range(100):
    game.reset()
    for _ in range(game.num_rounds):
        game.round()


for ps in game.players:
    print(f"{ps.player.name}: {ps.score}")








