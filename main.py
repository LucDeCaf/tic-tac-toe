from board_manager import BoardManager


def main():
    board_manager: BoardManager = BoardManager()
    play_again: bool = board_manager.play_round()

    while play_again:
        play_again = board_manager.play_round()


if __name__ == "__main__":
    main()
