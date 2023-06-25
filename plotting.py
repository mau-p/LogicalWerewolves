import pandas as pd
import matplotlib.pyplot as plt

stats = pd.read_csv('stats.csv')

# Plot winrate
winrate = stats.pivot(index='n_werewolves', columns=['higher_order', 'dynamic_behavior'], values='winrate')
winrate.plot()
plt.title('Winrate of agents')
plt.xlabel('Number of werewolves')
plt.ylabel('Winrate')
plt.savefig('winrate.png')
# plt.show()
plt.clf()

# Plot correct score
correct_score = stats.pivot(index='n_werewolves', columns=['higher_order', 'dynamic_behavior'], values='correct_score')
correct_score.plot()
plt.title('Amount of correct knowledge updates of agents')
plt.xlabel('Number of werewolves')
plt.ylabel('Correct score') 
plt.savefig('correct_score.png')
# plt.show()
plt.clf()

# Plot number of rounds
n_rounds = stats.pivot(index='n_werewolves', columns=['higher_order', 'dynamic_behavior'], values='num_rounds')
n_rounds.plot()
plt.title('Number of rounds played by agents')
plt.xlabel('Number of werewolves')
plt.ylabel('Number of rounds')
plt.savefig('n_rounds.png')
# plt.show()
plt.clf()