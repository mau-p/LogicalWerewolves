import argparse
import game
import pandas as pd
from tqdm import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    total_agents = 20
    args = parser.parse_args()
    n_games = 500
    stats = pd.DataFrame(columns=['knowledge_order', 'n_werewolves', 'winrate', 'correct_score', 'num_rounds'])

    for n_werewolves in range(1, 5):
        for knowledge_order in range(1, 11):
            winrate = 0
            correct_score = 0
            num_rounds = 0
            for _ in range(n_games):
                game_instance = game.Game(knowledge_order=knowledge_order, number_werewolves=n_werewolves, number_villagers=total_agents-n_werewolves-1)
                winrate_single, correct_score_single, num_rounds_single = game_instance.run_game()
                winrate += winrate_single
                correct_score += correct_score_single
                num_rounds += num_rounds_single
            stats = pd.concat([stats, pd.DataFrame({'knowledge_order': [knowledge_order], 'n_werewolves': [n_werewolves], 'winrate': [winrate/n_games], 'correct_score': [correct_score/n_games], 'num_rounds': [num_rounds/n_games]})], ignore_index=True)
    stats.to_csv('stats.csv')   