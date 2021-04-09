from Classes.player import player
from Classes.Card import Card
import gym
import random

class Take6(gym.Env):
        def __init__(self,players):
            '''
            Parameters
            ----------
            players : List
                List containing player instances

            Returns
            -------
            None.
            Initializes the Take6 environment

            '''
            self.players = players  # List of players in the game
            self.deck = [Card(i) for i in range(1,105)]#initialize the deck
            #print(self.deck)
            self.deal_hands()
            self.initialize_board()

        def deal_hands(self):
            '''
            Returns
            -------
            None.
            Deal hands of 10 cards to the players in the game
            '''
            for p in players:
                p.board = random.sample(self.deck,10)
                for card in p.board:
                    self.deck.remove(card)

        def initialize_board(self):
            pass
