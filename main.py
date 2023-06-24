import argparse
import game

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('knowledge_order', type=int, nargs='?', default=2, help='Higher order knowledge')
    parser.add_argument('n_werewolves', type=int, nargs='?', default=2, help='Number of werewolves')
    parser.add_argument('n_villagers', type=int, nargs='?', default=8, help='Number of villagers')
    total_agents = 20
    args = parser.parse_args()
    n_games = 500

    winrate = 0
    correct_score = 0
    num_rounds = 0
    for _ in range(n_games):
        game_instance = game.Game(knowledge_order=args.knowledge_order, number_werewolves=args.n_werewolves, number_villagers=args.n_villagers)
        winrate_single, correct_score_single, num_rounds_single = game_instance.run_game()
        winrate += winrate_single
        correct_score += correct_score_single
        num_rounds += num_rounds_single
    print(f'Knowledge order: {args.knowledge_order}, Winrate over {n_games}: {winrate/n_games}, Average correct update score: {correct_score/n_games}, Average number of rounds: {num_rounds/n_games}')