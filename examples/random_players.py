
from kravy import Game
from kravy.players import RandomPlayer
import logging

# setup logging
logging.basicConfig(level="INFO")

# setup a game
game = Game(
    [
        RandomPlayer("A"),
        RandomPlayer("B", take_min=True),
    ]
)

# play some rounds
for _ in range(1000):
    game.reset()
    for _ in range(game.num_rounds):
        game.round()

# print final score
for ps in game.players:
    print(f"{ps.player.name}: {ps.score}")


