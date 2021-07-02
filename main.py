## This is the main file to evaluate the results and make some plots for my report.


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

factors = [0.2,0.4,0.6,0.8,1.0]  #testing the impact of confidence factor C
r = 500000
thrown1 = []
thrown2 = []
for c in factors :
    ai = MCTS(num_players = 2,confidence = c)
    t1=time.time()
    ai.train(printing=False, nb_rounds=r)
    t2=time.time()
    print('ELAPSED TIME : ' +str(t2-t1))
    def play(n_games = 1):
        states = []
        score= []
        n_ties = 0
        los = {'AI':0, 'opp':0}
        for n in range(n_games):

            stop = False
            ai.game.determ_init_state(ai.fixed_hand,ai.fixed_board)
            ai.reset()

            while not stop:

                act = []
                move = ai.play()

                act.append(move)
                for p in range(1,len(ai.game.players)):
                    actions = ai.game.get_actions(ai.game.state,ai.game.players[p])
                    action = np.random.choice(actions)
                    act.append(action)
                state = deepcopy(ai.game.state)
                states.append(state)
                reward,stop,winner = ai.game.step(act)

            if len(winner)>1:
                n_ties+=1
            if 0 in winner:
                los['AI']+=1
            else:
                los['opp']+=1

            states.append(deepcopy(ai.game.state))

        print("Number of ties : ",n_ties)
        return states,score,los
    n_games = 500
    results = []
    batch = 5
    mean_val = {'AI':[], 'opp':[]}
    for p in range(batch):
        states,score,los = play(n_games = n_games)
        mean_val['AI'].append(los['AI'])
        mean_val['opp'].append(los['opp'])

    for u in mean_val:
        mean_val[u]=np.mean(mean_val[u])
    thrown1.append(mean_val['AI'])
    thrown2.append(mean_val['opp'])


        

title = 'Mean number of games won on ' +str(n_games)+" games with 4 players"

labels = [str(i) for i in factors]

thrown1


x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, thrown1, width, label='AI trained with Monte Carlo')
rects2 = ax.bar(x + width/2, thrown2, width, label='Random policy player')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Number of games won')
ax.set_xlabel('Number of iterations during training')
ax.set_title(title)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.show()
