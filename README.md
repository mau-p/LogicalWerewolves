# LogicalWerewolves

This code is a logical implementation of the game Werewolves of Miller's Hollow. It simulates the knowledge of different agents and different voting strategies using higher-order and announcement logic. 

The website of the project containing further information about the logical formalization of the game can be found [here](https://mau-p.github.io/LogicalWerewolves/ "Visit project site").

## Running the code

Running the code in python requires three command line arguments: whether to use higher-order knowledge (0 or 1), whether to use dynamic behavior (0 or 1), the number of werewolves and the number of villagers. The code can then be run as follows:

```
python3 main.py <higher_order> <dynamic_behavior> <n_werewolves> <n_villagers>
```

Running this will run the game 500 times and return the average winrate, correct score and number of rounds.

Additionally, to run a single game:

```
python3 main_demo.py <higher_order> <dynamic_behavior> <n_werewolves> <n_villagers>
```