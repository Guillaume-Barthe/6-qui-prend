# main file

from Classes.Card import Card
from Classes.Take6 import Take6
from Classes.player import player
import gym

u = Card(5)
print(u)
players = [player(True)]

game = Take6(players)
