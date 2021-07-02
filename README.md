# 6-qui-prend

This repository presents the implementation of a reinforcement learning agent capable of playing **the card game Skyjo.**

How it works
======

My code is divided in multiple .py files that represent each class of the environment. I created 3 different classes, the **player** class is written in player.py and described each player in the game. The **card** class is written in card.py and described each card of the deck. The **take6** class in Take6.py is the most important one where the environment is written. Those three classes are in the classes file. In the MCTS.py file you can find the implementation of the Monte Carlo Tree Search algorithm used here to train on the environment. 

The Environment
======

I implemented an environment from scratch  that does not fit well known implementations like the Gym implementation of environments. Therefore, it is a custom environment where the action_space and the observation_space have custom shapes. I do not a have a display() method to visualize a game but it is an interesting improvement that could be added to this repository.

Main file
======

In order to run training and play with the agent, you can use the main.py file. In there I imported the agent from MCTS.py and used it for training. As it is right now, all the code is used for plotting results that were used in my report, but you can easily play with this file to try other configurations of training and testing

Please note that the most important lines to initialize our environment are : 

ai = MCTS(num_players = 2,confidence = c)
ai.game.determ_init_state(ai.fixed_hand,ai.fixed_board)


Play with parameters
======

In the main.py file you can play with the different parameters that are used for both training and testing. I mainly used 500.000 iterations but you can change this to the value that suits you best and you can also play with the confidence factor C that is an input of the MCTS agent.

