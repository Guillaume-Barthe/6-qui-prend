## This is the implementation of the Monte Carlo Tree Search


from Classes.Take6 import Take6,Agent
from Classes.Node import Node
import random
import numpy as np
from copy import deepcopy
from Classes.Card import Card

class MCTS(Agent):

    def __init__(self, environment=Take6,num_players = 2,confidence = 1):
        self.game = environment(num_players = num_players)
        self.fixed_hand = [Card(5),Card(70),Card(12),Card(35),Card(24),Card(27),Card(31),Card(85),Card(61),Card(94)]
        self.fixed_board = board = np.zeros((4,6)).astype(int)
        self.fixed_board[0][0]=36
        self.fixed_board[1][0]=13
        self.fixed_board[2][0]=93
        self.fixed_board[3][0]=47
        self.game.determ_init_state(self.fixed_hand,self.fixed_board)
        self.trees = dict()
        self.root = Node(is_root=True, state=self.game.state) # a tree node with no parent
        self.current_node = self.root #initialize at the root
        #self.fixed_hand = deepcopy(self.game.players[0].hand)
        #self.fixed_board = deepcopy(self.game.board)
        self.nb_games = 0
        self.C = confidence

    def reset(self):
        self.current_node = self.root

    def train_continous(self, nb_rounds = 10,printing=False):
        while not final:
            root = Node(is_root = True, state = self.game.state)
            current_node = deepcopy(root)
            player = deepcopy(self.game.players[0])
            available_actions = self.game.get_actions(current_node.state,player)
            known_actions = current_node.children.keys()
            unknown_actions = list(set(available_actions) - set(known_actions))

            if unknown_actions == []:
                if printing:
                    print('node fully expanded: choose next with UCT')
                #compute next move according to the MCTS algorithm with UCT
                action = self.next_move(self.C)
                moves = [action]
                current_node = self.current_node.children[action]
                for p in range(1,len(self.game.players)):
                    adversary_actions = self.game.get_actions(self.current_node.state,self.game.players[p])
                    adv_action = np.random.choice(adversary_actions)
                    moves.append(adv_action)

                reward, final,_ = self.game.step(moves)


            # unknown tree area: need to expand the tree
            else:
                if printing:
                    print('node not fully expanded: explore and expand')
                # find an action that has not been explored
                action = unknown_actions[0]
                child= self.expand(self.current_node, action) # play default policy until the end to get a reward
                self.current_node = child

                # simulate the end of the game with random plays
                reward = self.simulate()

                if printing:
                    print('node expanded')

                final = True

        # game is over, reward is collected, now we backpropagate it on the path

        self.backpropagate(self.current_node, reward) # backprop the rewards up in the tree
        if printing:
            print('reward backpropagated from child')
            #self.game.display()





    def train(self, nb_rounds=10, printing=True):
        for n in range(nb_rounds):
            # start a game
            self.game.determ_init_state(self.fixed_hand,self.fixed_board)
            #self.game.board = deepcopy(self.fixed_board)
            #self.game.players[0].hand = [u for u in self.fixed_hand]
            self.current_node = self.root
            final = False

            if n%1000 == 0:
                print('entering game number '+str(n))
            while not final:

                available_actions = self.game.get_actions(self.current_node.state,self.game.players[0])
                known_actions = self.current_node.children.keys()
                unknown_actions = list(set(available_actions) - set(known_actions))


                # known tree area:
                if unknown_actions == []:
                    if printing:
                        print('node fully expanded: choose next with UCT')
                    #compute next move according to the MCTS algorithm with UCT
                    action = self.next_move(self.C)
                    moves = [action]
                    self.current_node = self.current_node.children[action]
                    for p in range(1,len(self.game.players)):
                        adversary_actions = self.game.get_actions(self.current_node.state,self.game.players[p])
                        adv_action = np.random.choice(adversary_actions)
                        moves.append(adv_action)

                    reward, final,_ = self.game.step(moves)


                # unknown tree area: need to expand the tree
                else:
                    if printing:
                        print('node not fully expanded: explore and expand')
                    # find an action that has not been explored
                    action = unknown_actions[0]
                    child= self.expand(self.current_node, action) # play default policy until the end to get a reward
                    self.current_node = child

                    # simulate the end of the game with random plays
                    reward = self.simulate()


                    if printing:
                        print('node expanded')

                    final = True

            # game is over, reward is collected, now we backpropagate it on the path

            self.backpropagate(self.current_node, reward) # backprop the rewards up in the tree
            if printing:
                print('reward backpropagated from child')
                #self.game.display()

            self.nb_games +=1






    def next_move(self,C):
        """
        returns the next move (integer action) given a board state (Node object)
        """
        values = dict()
        ## TODO:  implement UCT decision with C_p = 1.
        for action, child in self.current_node.children.items():
            child.compute_value()
            values[action] = round(child.Q +C*child.U,2)
        #if self.nb_games % 1000 == 0 :
            #print(values)
            #test_action = max(values, key=(lambda k: values[k]))
            #print("The chosen card for action "+str(test_action)+" is a "+str(self.game.players[0].hand[test_action]))


        chosen_action = max(values, key=(lambda k: values[k]))
        return chosen_action


    def backpropagate(self, expanded_node, reward):
        """ propagates back the value received by the expanded node following rollout"""

        current_node = expanded_node

        while not current_node.is_root:

#             self.game.display(states=current_node.state)

            current_node.nb_wins += reward


            current_node.nb_games += 1
            current_node = current_node.parent
            #reward *= -1 # propagate opposite values along the path for each player



    def expand(self, current_node, move):
        """
        move into chosen child state (node created created)
        """
        # add a node ...
        child = Node(parent=current_node)
        child.nb_games = 1 # it is being played
        current_node.add_child(child, move)
        moves = [move]
        for p in range(1,len(self.game.players)):
            adversary_actions = self.game.get_actions(current_node.state,self.game.players[p])
            adv_action = np.random.choice(adversary_actions)
            moves.append(adv_action)
        state = self.game.get_transition(current_node.state, moves)
        child.set_state(state)


        return child


    def simulate(self):
        test,rew,_ = self.game.is_terminal()
        if test:
            if 0 in rew:
                return 1
            else:
                return 0
        finale = False
        while not finale:
            act = []
            for player in self.game.players:
                actions = self.game.get_actions(self.game.state,player)
                action = np.random.choice(actions)
                act.append(action)
            reward, finale,_ = self.game.step(act)

        return reward

    def play(self):
        available_actions = self.game.get_actions(self.game.state,self.game.players[0])
        known_actions = self.current_node.children.keys()
        unknown_actions = list(set(available_actions) - set(known_actions))

        # known tree area:
        if unknown_actions == []:

            #compute next move according to the MCTS algorithm with UCT
            action = self.next_move(self.C)
            self.current_node = self.current_node.children[action]


        # unknown tree area: need to expand the tree
        else:
            # find an action that has not been explored

            action = np.random.choice(unknown_actions)



        return action
