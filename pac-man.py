import sys
from parser import load_config
from game import Game


def main():
    if len(sys.argv) != 2:
        print("Usage: python pac-man.py <config_file>")
        sys.exit(1)

    try:
        parsing_result = load_config(sys.argv[1])
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    else:
        print("Config loaded successfully.")
        game = Game(parsing_result)
        game.run()


if __name__ == "__main__":
    main()
