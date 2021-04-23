from Classes.player import player
from Classes.Card import Card
import gym
import random
import numpy as np


class Take6():
        def __init__(self,training = True, training_policy = None, adversary_policy=None):

            if training :
                self.player = Agent(self,training_policy)
            else :
                pass #HumanPlay
            self.adversary = Agent(self,adversary_policy)
            self.players = [self.player,self.adversary]
            self.deck = [Card(i) for i in range(1,105)]#initialize the deck
            self.deal_hands()
            self.board = self.init_board()
            self.state = self.init_state()
            self.print_state()

        def print_state(self):
            print('\n')
            print("Board : ")
            print(self.board)
            print('\n')
            print("Hand player 1 : ")
            print(self.players[0].hand)
            print('\n')
            print("Hand player 2 : ")
            print(self.players[1].hand)
            print('\n')
            print("Actual state : ")
            print(self.state)
            print('\n')

        def deal_hands(self):
            '''
            Returns
            -------
            None.
            Deal hands of 10 cards to the players in the game
            '''
            for p in self.players:
                p.hand = random.sample(self.deck,10)
                for card in p.hand:
                    self.deck.remove(card)

        def init_board(self):
            board = np.zeros((4,6)).astype(int)
            for i in range (4):
                random_card = random.sample(self.deck,1)[0]
                self.deck.remove(random_card)
                board[i][0]=random_card.value
            return board

        def init_state(self):
            return [card.value for card in self.player.hand]+[self.board]

        def get_actions(self,state):
            pass

class Agent:
    '''
    Default policy is random.
    '''
    def __init__(self, environment, policy=None):
        if policy:
            self.policy = policy
        else:
            self.policy = self.random_policy
        self.environment = environment

    def random_policy(self, state):
        actions = self.environment.get_actions(state)
        probs = np.ones(len(actions)) / len(actions)
        return probs, actions

    def get_action(self, state):
        action = None
        probs, actions = self.policy(state)
        if len(actions):
            i = np.random.choice(len(actions), p=probs)
            action = actions[i]
        return action

