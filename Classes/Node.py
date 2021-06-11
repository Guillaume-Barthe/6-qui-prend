import random
import numpy as np
class Node:
    def __init__(self,state=None, parent=None, is_root=False,prior=0):
        self.state = state # store the couple (player, board)
        self.children = {}
        self.parent = parent
        self.nb_games = 1
        self.nb_wins = 0
        self.is_root = is_root
        self.prior = prior  # float
        self.total_value = 0  # float


    def add_child(self, child, action):
        """
        add a child in the form of a dictionary entry indexed by the action that leads to it
        child: Node object
        action: integer
        """
        self.children[action] = child
        child.set_parent(self)

    def compute_value(self):
        """
        value as given by the UCT algorithm
        """

        self.Q = self.nb_wins / (self.nb_games)
        self.U = np.sqrt(2*np.log(self.parent.nb_games) / (self.nb_games))
        return self

    def set_parent(self, parent):
        """
        parent is a Node object that has self as a child
        """
        self.parent = parent

    def set_value(self,val):
        self.value = val

    def set_state(self, state):
        self.state = state
