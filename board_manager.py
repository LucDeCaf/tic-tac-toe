from turn_handler import TurnHandler


class BoardManager:
    def __init__(self, p1_winstreak: int = 0, p2_winstreak: int = 0):
        # Create board
        self.board: list = [['-' for _ in range(3)] for _ in range(3)]

        # Assign winstreaks based on input values
        self.player_one_winstreak: int = p1_winstreak
        self.player_two_winstreak: int = p2_winstreak

        # Initialize winner
        self.winner: int = 0

        # Handle game flow
        self.game_running: bool = True
        self.is_two_player: str = ''

        # Initialize winning configurations
        self.WINNING_POSITIONS: tuple = (
            # Horizontal wins
            ((0, 0), (0, 1), (0, 2)),
            ((1, 0), (1, 1), (1, 2)),
            ((2, 0), (2, 1), (2, 2)),
            # Vertical wins
            ((0, 0), (1, 0), (2, 0)),
            ((0, 1), (1, 1), (2, 1)),
            ((0, 2), (1, 2), (2, 2)),
            # Diagonal wins
            ((0, 0), (1, 1), (2, 2)),
            ((2, 0), (1, 1), (0, 2))
        )

        # Initialize Turn Handler
        self.turn_handler: TurnHandler = TurnHandler(board=self.board, win_pos=self.WINNING_POSITIONS)

    def check_for_win(self) -> int:
        """If current board configuration contains a won/lost/drawn position, print board and result and return True."""
        for pos in self.WINNING_POSITIONS:
            # If any player wins, reset the other player's winstreak and add one to the winning player's winstreak
            if pos[0] in self.turn_handler.player_one_moves and pos[1] in self.turn_handler.player_one_moves and pos[2]\
                    in self.turn_handler.player_one_moves:
                self.player_one_winstreak += 1
                self.player_two_winstreak = 0
                self.display_board()
                self.winner = 1
                print(">>> Player One wins! <<<")
                return True

            if pos[0] in self.turn_handler.player_two_moves and pos[1] in self.turn_handler.player_two_moves and pos[2]\
                    in self.turn_handler.player_two_moves:
                self.player_one_winstreak = 0
                self.player_two_winstreak += 1
                self.display_board()
                self.winner = 2
                print(">>> Player Two wins! <<<")
                return True

            # If there is a draw, reset both player's winstreaks
            if not self.turn_handler.open_spaces:
                self.player_one_winstreak = 0
                self.player_two_winstreak = 0
                self.display_board()
                self.winner = 0
                print(">>> Draw. <<<")
                return True

        # Return False if there is no Win, Loss, or Draw in the current position
        return False

    def display_board(self) -> None:
        """Prints board to console."""
        for row in self.board:
            display_str: str = ''
            for item in row:
                display_str += f'{item} '
            print(display_str)

    def reset_board(self, p1_winstreak: int, p2_winstreak: int):
        """Resets the board and resets open spaces"""
        # Reinitialize the board, but parse through the given winstreaks
        self.__init__(p1_winstreak, p2_winstreak)

    def play_round(self) -> bool:
        """Plays a round of Tic Tac Toe. """
        # Decides whether to play PvP or PvC
        self.is_two_player = input('Do you want to play a two-player game? Enter "y/n": ')

        while not self.is_two_player == 'y' and not self.is_two_player == 'n':
            self.is_two_player = input('Please enter "y/n": ')

        while self.game_running:
            self.display_board()

            # Check if player one wins or draws
            if not self.turn_handler.player_turn(1):
                continue

            if self.check_for_win():
                break

            # Check if player two / computer wins or draws
            if self.is_two_player == 'y':
                self.display_board()
                self.turn_handler.player_turn(2)
            else:
                self.turn_handler.computer_turn()

            if self.check_for_win():
                break

        # Display the relevant winning streak of the winning player. If there is no winning player, display nothing
        match self.winner:
            case 1:
                print(f"Winning streak: {self.player_one_winstreak}")
            case 2:
                print(f"Winning streak: {self.player_two_winstreak}")

        # Check if player wants to play another round and return the answer as True or False
        new_round: str = input("\nPlay again? Enter 'y/n', or enter 'r' to reset the scores and play a new round: ")
        while not new_round == 'y' and not new_round == 'n' and not new_round == 'r':
            new_round = input("Please only enter 'y/n/r': ")

        # If 'y', reset the board and return True. If 'n', reset the board and return False. If 'r', reinitialize the
        # winstreaks, reset the board, and return True.
        match new_round:
            case 'y':
                self.reset_board(self.player_one_winstreak, self.player_two_winstreak)
                return True
            case 'r':
                self.reset_board(0, 0)
                return True
            case 'n':
                return False