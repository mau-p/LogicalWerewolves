import argparse
import game


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('n_werewolves', type=int, nargs='?', default=2, help='Number of werewolves')
    parser.add_argument('n_villagers', type=int, nargs='?', default=4, help='Number of villagers')
    args = parser.parse_args()
    game_instance = game.Game(number_werewolves=args.n_werewolves, number_villagers=args.n_villagers)
    game_instance.run_game()


if __name__ == "__main__":
    main()
