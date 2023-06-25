import argparse
import game
import pandas as pd
from tqdm import tqdm

if __name__ == "__main__":
    true_false = [False, True]
    total_agents = 20
    n_games = 500
    stats = pd.DataFrame(columns=['higher_order', 'dynamic_behavior', 'n_werewolves', 'winrate', 'correct_score', 'num_rounds'])
    stats['higher_order'] = stats['higher_order'].astype(bool)
    stats['dynamic_behavior'] = stats['dynamic_behavior'].astype(bool)

    for higher_order in true_false:
        print(f"Higher order: {higher_order}")
        for dynamic_behavior in true_false:
            print(f"Dynamic behavior: {dynamic_behavior}")
            if dynamic_behavior and not higher_order:
                continue
            for n_werewolves in tqdm(range(1, total_agents//2)):
                winrate = 0
                correct_score = 0
                num_rounds = 0
                for _ in range(n_games):
                    game_instance = game.Game(number_werewolves=n_werewolves,
                                            number_villagers=total_agents-n_werewolves-1,
                                            higher_order=higher_order, dynamic_behavior=dynamic_behavior)
                    winrate_single, correct_score_single, num_rounds_single = game_instance.run_game()
                    winrate += winrate_single
                    correct_score += correct_score_single
                    num_rounds += num_rounds_single
                stats = pd.concat([stats, pd.DataFrame({'higher_order': [higher_order], 'dynamic_behavior': [dynamic_behavior], 'n_werewolves': [n_werewolves], 'winrate': [winrate/n_games], 'correct_score': [correct_score/n_games], 'num_rounds': [num_rounds/n_games]})], ignore_index=True)
    stats.to_csv('stats.csv', index=False)