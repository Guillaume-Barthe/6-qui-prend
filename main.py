# main file

from Classes.Card import Card
from Classes.Take6 import Take6
from Classes.player import player
import gym
from copy import deepcopy
import numpy as np
from Classes.MCTS import MCTS
import random
import time
import matplotlib.pyplot as plt

rounds = [100000]
sc = []
err = []
for r in rounds :
    ai = MCTS()
    t1=time.time()
    ai.train(printing=False, nb_rounds=r)
    t2=time.time()
    print('ELAPSED TIME : ' +str(t2-t1))
    def play(n_games = 1):
        states = []
        score = []
        los = []
        for n in range(n_games):

            stop = False
            ai.game.determ_init_state(ai.fixed_hand,ai.fixed_board)
            ai.reset()

            while not stop:
                #print(ai.game.board)
                #print(ai.game.players[0].hand)
                act = []
                move = ai.play()
                #print(move)
                act.append(move)
                for p in range(1,len(ai.game.players)):
                    actions = ai.game.get_actions(ai.game.state,ai.game.players[p])
                    action = np.random.choice(actions)
                    act.append(action)
                state = deepcopy(ai.game.state)
                states.append(state)
                reward,stop,winner = ai.game.step(act)
            los.append(winner)
            score.append(reward)
            states.append(deepcopy(ai.game.state))
            #for p in env.players:
                #print(p.score)
        return states,score,los
    n_games = 2
    results = []
    batch = 2
    for p in range(batch):
        states,score,los = play(n_games = n_games)
        results.append(np.sum(score))
        print(los)

        #print("Nombre de parties gagnées : " + str(np.sum(score))+" / "+ str(n_games))
    #print(results)
    print("Score moyen sur " + str(batch)+ " batch de "+str(n_games)+" parties : "+str(np.mean(results)))
    print("Standard deviation : " +str(np.std(results)))
    sc.append(np.mean(results))
    err.append(np.std(results))
plt.scatter(rounds,sc)
plt.errorbar(rounds,sc,err,linestyle='None')
plt.show()
