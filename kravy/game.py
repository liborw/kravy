
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import copy
import random
import logging




@dataclass(eq=True, order=True)
class Card:
    """
    Card object consist of card value and number of
    points, that player recieves in case of taking
    row containing this card.
    """

    value: int
    points: int

    def __repr__(self) -> str:
        return f"{self.value}|{self.points}"


def default_deck() -> list[Card]:
    """Standard deck for 6 nimmt game."""
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


class Player(ABC):

    def __init__(self, name: str):
        self.name: str = name
        self.log = logging.getLogger(name)

    @abstractmethod
    def select_card(self, hand: list[Card], rows: list[list[Card]]) -> Card:
        pass

    @abstractmethod
    def select_row(self, rows: list[list[Card]]) -> int:
        pass


@dataclass
class PlayerState(object):
    """
    Object representing a player state in the game.
    It consists of the actual player, his hand, score
    and selected card.
    """
    player: Player
    hand: list[Card] = field(default_factory=list)
    score: int = 0
    card: Card|None = None

    def __repr__(self):
        return f"{self.player.name} ({self.score}): {self.hand}"


class Game():
    """
    Implementation of the 6 nimmt game.
    """

    def __init__(self,
                 players: list[Player],
                 deck: list[Card]|None = None,
                 num_rounds: int = 10,
                 num_rows: int = 4
                 ):
        self.num_rounds = num_rounds
        self.num_rows = num_rows
        self.deck = deck if deck else default_deck()
        self.log = logging.getLogger("game")

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
        min_d = float("inf")
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
        self.log.info(f"state: {self.rows}")

        for ps in self.players:
            ps.card = ps.player.select_card(
                    copy.deepcopy(ps.hand),
                    copy.deepcopy(self.rows)
            )

        lowest = self.lowest()
        for ps in sorted(self.players, key=lambda ps: ps.card):
            ps.hand.remove(ps.card)
            self.log.info(f"{ps.player.name} chosed {ps.card}")

            if ps.card < lowest:
                self.log.info(f"{ps.card} is lower that all rows")
                row_idx = ps.player.select_row(copy.deepcopy(self.rows))
                points = self.row_points(row_idx)
                ps.score += points
                self.log.info(f"{ps.player.name} chosed to take {row_idx} row with {points} points")
                self.rows[row_idx] = [ps.card]
                continue

            row_idx = self.find_closest_row_idx(ps.card)
            if len(self.rows[row_idx]) >= 5:
                points = self.row_points(row_idx)
                ps.score += points
                self.log.info(f"{ps.card} will go on {row_idx} and is sixth and get {points} points")
                self.rows[row_idx] = [ps.card]
                continue

            self.log.info(f"{ps.card} will go on {row_idx} and is safe")
            self.rows[row_idx].append(ps.card)


