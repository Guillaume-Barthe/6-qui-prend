from Classes.player import player
from Classes.Card import Card
import gym
import random
import numpy as np
from copy import deepcopy


class Take6():
        def __init__(self,training = True, training_policy = None, adversary_policy=None, num_players = 2):
            self.training_policy = training_policy
            self.adversary_policy = adversary_policy
            self.training = training
            self.num_players = num_players
            self.play = 0
            self.state = self.init_state()


        def print_state(self):
            print('\n')
            print("Board : ")
            print(self.board)
            print('\n')
            print("Hand player 1 : ")
            print(self.players[0].hand)
            print('\n')
            print("Min card Hand player 1 : ")
            print(self.players[0].min_card())
            print('\n')
            print("MAX card Hand player 1 : ")
            print(self.players[0].max_card())
            print('\n')
            print("Hand player 2 : ")
            print(self.players[1].hand)
            print('\n')
            print("Actual state : ")
            print(self.state[:len(self.state)-1])
            print('\n')
            print("Edge cards : ")
            print(self.edge_cards())
            print('\n')


        def deal_hands(self):
            '''
            Returns
            -------
            None.
            Deal hands of 10 cards to the players in the game
            '''
            if len(self.deck)<(len(self.players)*10)+4:     #Number of cards to deal + the cards on the board
                self.deck = [Card(i) for i in range(1,105)]
            for p in self.players:
                p.hand = random.sample(self.deck,10)
                for card in p.hand:
                    self.deck.remove(card)

        def edge_cards(self):
            '''
            Returns
            -------
            None.
            Returns the values of the four cards on the edge of the board. Those that are important when placing your next card
            '''
            #print(self.state[len(self.state)-1])
            #x_,y_ = np.where(self.state[len(self.state)-1] != 0)
            #edge_positions = [(x, y) for x, y in zip(x_, y_)]
            x_0 = np.argmax(self.state[len(self.state)-1][0])
            x_1 = np.argmax(self.state[len(self.state)-1][1])
            x_2 = np.argmax(self.state[len(self.state)-1][2])
            x_3 = np.argmax(self.state[len(self.state)-1][3])
            edge_positions = [(0,x_0),(1,x_1),(2,x_2),(3,x_3)]


            return edge_positions



        def init_board(self):
            board = np.zeros((4,6)).astype(int)
            for i in range (4):
                random_card = random.sample(self.deck,1)[0]
                self.deck.remove(random_card)
                board[i][0]=random_card.value
            return board

        def determ_init_state(self,hand,board):
            self.player = Agent(self,self.training_policy)
            self.players = [self.player]
            for p in range(self.num_players-1):
                self.players.append(Agent(self,self.adversary_policy))
            out = []
            for u in hand:
                out.append(u.value)
            out.append(board[0][0])
            out.append(board[1][0])
            out.append(board[2][0])
            out.append(board[3][0])
            self.deck = []
            for i in range (1,105):
                if i not in out:
                    self.deck.append(Card(i))
            self.players[0].hand = deepcopy(hand)
            self.board = deepcopy(board)
            for p in range (1,len(self.players)):
                self.players[p].hand = random.sample(self.deck,10)
                for card in self.players[p].hand:
                    self.deck.remove(card)
            self.state = [card.value for card in self.player.hand]+[self.board]
            return self.state





        def init_state(self):
            if self.training :
                self.player = Agent(self,self.training_policy)
            else :
                pass #HumanPlay
            self.players = [self.player]
            for p in range(self.num_players-1):
                self.players.append(Agent(self,self.adversary_policy))
            self.deck = [Card(i) for i in range(1,105)]#initialize the deck
            self.deal_hands()
            self.board = self.init_board()
            self.state = [card.value for card in self.player.hand]+[self.board]
            return self.state

        def re_init_state(self):
            self.deal_hands()
            self.board = self.init_board()
            self.state = [card.value for card in self.player.hand]+[self.board]
            return self.state

        def get_actions(self,state,player):
            hand = player.hand
            actions = [i for i in range(len(hand))]
            return actions

        def is_terminal(self):
            done = False
            scores = [self.players[p].score for p in range(len(self.players))]
            loser_score = np.max(scores)
            loser = np.argmax(scores)
            winner = np.argmin(scores)
            if len(self.player.hand)==0:
                done = True
                #print("player "+str(player)+' has lost with a score of '+str(loser_score)+' versus ' +str(np.min(scores)))
            #elif len(self.player.hand)==0 and loser_score<66 :
                #print("This round has ended and the scores are : "+str(scores))
                #self.re_init_state()

            return done,loser,winner

        def get_value(self,value):
            lastdigit = int(str(value)[-1])
            if value == 55:
                cost = 7    #PARTICULAR 55 Card
            elif value ==0:
                cost = 0
            elif value%11 == 0:
                cost = 5
            elif lastdigit == 5:
                cost = 2
            elif lastdigit == 0:
                cost = 3
            else:
                cost = 1
            return cost

        def get_rows_score(self):
            row0 = self.board[0]
            row1 = self.board[1]
            row2 = self.board[2]
            row3 = self.board[3]
            score0,score1,score2,score3  = 0,0,0,0
            for u in row0:
                score0+= self.get_value(u)
            for u in row1:
                score1+= self.get_value(u)
            for u in row2:
                score2+= self.get_value(u)
            for u in row3:
                score3+= self.get_value(u)
            return [score0,score1,score2,score3]

        def place_card(self,card):
            min = 150
            row = -1
            edge_pos = self.edge_cards()
            #print(edge_pos)
            edge_cards = [self.board[u] for u in edge_pos]
            score = 0
            for i in range(len(edge_cards)):
                value = edge_cards[i]
                if 0 < card - value < min:
                    row = i
                    min = card - value
            if min == 150:
                scores = self.get_rows_score()
                row = np.argmin(scores)
                col = 0
                score = scores[row]
                #print('A line was took and was worth ' + str(score)+" points")
                self.board[row]=[0,0,0,0,0,0]
            else :
                col = edge_pos[row][1]+1
            #print(card,min,row,col)
            if col == 5:
                for u in self.board[row]:
                    score+= self.get_value(u)

                #print('A line was took and was worth ' + str(score)+" points")
                #print(self.board[row])
                #score = 3
                self.board[row] = [card,0,0,0,0,0]
            else:
                self.board[(row,col)]=card
            return score

        def get_transition(self,state,actions):
            cards = []
            for a in range(len(actions)):
                player = self.players[a]
                action = actions[a]
                card = player.hand[action]
                player.hand.remove(card)
                cards.append(card.value)
            compteur = 0
            while compteur<len(self.players) :
                min_card = np.min(cards)
                i_min = np.argmin(cards)
                cards[i_min]=105 ##dont take that card into account anymore
                score = self.place_card(min_card)
                compteur+=1
                if score>0:
                    #print('A line was took by player '+str(i_min)+ ' and was worth ' + str(score)+" points")
                    self.players[i_min].score+=score

            state = [card.value for card in self.players[0].hand]+[self.board]
            return state


        def step(self,actions):
            state = deepcopy(self.state)
            #print(state)
            self.state = self.get_transition(state,actions)
            bool,loser,winner = self.is_terminal()
            if bool:
                if winner == 0:
                    reward = 1
                else:
                    reward = 0
            else:
                reward = 0
            return reward,bool,winner


class Agent:
    '''
    Default policy is random.
    '''
    def __init__(self, environment, is_machine, policy=None):
        if policy:
            self.policy = policy
        else:
            self.policy = self.random_policy
        self.environment = environment
        self.size_hand = 10
        self.hand = []
        self.is_machine = is_machine
        self.score = 0

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

    def max_card(self):
        max = 0
        for card in self.hand:
            if card.value > max:
                max = card.value
        return max

    def min_card(self):
        min = 104
        for card in self.hand:
            if card.value < min:
                min = card.value
        return min
