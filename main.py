from random import choice as random_choice

ALLOWED_NUMBERS: tuple = 1, 2, 3
WINNING_POSITIONS: tuple = (
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

OUTER_POSITIONS: tuple = (0, 1), (1, 0), (1, 2), (2, 1), (0, 0), (0, 2), (2, 0), (2, 2)


class Controller:
    def __init__(self, p1_winstreak: int = 0, p2_winstreak: int = 0):
        # Create board
        self.board: list = [['-' for _ in range(3)] for _ in range(3)]
        self.open_spaces: list = []
        self.update_open_spaces()

        # Per-round data
        self.winner: int = 0
        self.player_one_moves: list = []
        self.player_two_moves: list = []
        self.player_one_char: str = ''
        self.player_two_char: str = ''

        # Assign winstreaks based on input values
        self.player_one_winstreak: int = p1_winstreak
        self.player_two_winstreak: int = p2_winstreak

        # Handle game flow
        self.game_running: bool = True
        self.is_two_player: str = ''

    def check_for_win(self) -> int:
        """If current board configuration contains a won/lost/drawn position, print board and result and return True."""
        # If there is a draw, reset both player's winstreaks
        if not self.open_spaces:
            self.player_one_winstreak = 0
            self.player_two_winstreak = 0
            self.display_board()
            self.winner = 0
            print(">>> Draw. <<<")
            return True

        for pos in WINNING_POSITIONS:
            # If any player wins, reset the other player's winstreak and add one to the winning player's winstreak
            if pos[0] in self.player_one_moves and pos[1] in self.player_one_moves and pos[2] in self.player_one_moves:
                self.player_one_winstreak += 1
                self.player_two_winstreak = 0
                self.display_board()
                self.winner = 1
                print(">>> Player One wins! <<<")
                return True
            if pos[0] in self.player_two_moves and pos[1] in self.player_two_moves and pos[2] in self.player_two_moves:
                self.player_one_winstreak = 0
                self.player_two_winstreak += 1
                self.display_board()
                self.winner = 2
                print(">>> Player Two wins! <<<")
                return True
        # Return False if there is no Win, Loss, or Draw in the current position
        return False

    def change_state(self, pos: tuple | list, turn: int) -> bool:
        """Changes a position at a given tile if the tile is blank, i.e. has a value of '-'. Returns boolean based on
        whether the tile was empty or not."""
        # Check if chosen tile is empty
        if not self.board[pos[0]][pos[1]] == '-':
            return False

        # Change the tile to the given player's tile character and append to the given player's list of played moves
        match turn:
            case 1:
                self.board[pos[0]][pos[1]] = self.player_one_char
                self.player_one_moves.append(tuple(pos))
            case 2:
                self.board[pos[0]][pos[1]] = self.player_two_char
                self.player_two_moves.append(tuple(pos))

        # Update the list of open spaces to exclude the played move
        controller.update_open_spaces()
        return True

    def player_turn(self, player: int) -> bool:
        """Changes a tile on the board to player_one_char at position that player specifies. Returns boolean based on if
        the change was successful, i.e. valid coordinates were given. """
        # Get player's move
        player_moves: str = input('Enter a row and a column (Separation with a space is optional): ')

        # Get player moves in tuple form
        unfiltered_coords: tuple = tuple([move for move in player_moves])

        # Check if non-number characters are given
        try:
            semifiltered_coords: tuple = tuple([int(item) - 1 for item in unfiltered_coords])
        except ValueError:
            print('\n>>>> Please only enter the numbers 1, 2, or 3 <<<<')
            return False

        # Check if correct number of numbers are given
        if not len(semifiltered_coords) == 2:
            print('\n>>>> Please only enter 2 numbers. <<<<')
            return False

        # Filter out disallowed numbers
        filtered_coords: tuple = tuple([item for item in semifiltered_coords if item + 1 in ALLOWED_NUMBERS])
        print(filtered_coords)

        # Check if numbers above 3 were entered
        if not len(filtered_coords) == 2:
            print('\n>>>> Please only enter the numbers 1, 2, or 3 <<<<')
            return False

        if not self.change_state(pos=(filtered_coords[0], filtered_coords[1]), turn=player):
            print("\n>>>> Please enter a valid set of coordinates. <<<<")
            return False

        return True

    def find_winning_move(self, moves: tuple | list) -> list:
        """Returns any move that wins in 1 turn for a given list of moves that have already been made."""
        # Loop through all winning configurations and check if two of the moves are already played by one person.
        # Also, check if the final missing space is open or blocked. If it is open, return the final missing space.
        for config in WINNING_POSITIONS:
            if config[0] in moves and config[1] in moves and config[2] in self.open_spaces:
                return config[2]
            if config[0] in moves and config[2] in moves and config[1] in self.open_spaces:
                return config[1]
            if config[1] in moves and config[2] in moves and config[0] in self.open_spaces:
                return config[0]
        return []

    def computer_turn(self) -> None:
        """Changes tile on board to player_two_char at semi-random position."""
        # If computer can win in 1 move, play move in winning tile
        computer_move: list = self.find_winning_move(self.player_two_moves)
        if computer_move:
            self.change_state(pos=computer_move, turn=2)
            return

        # If player is 1 move from winning, make move in winning tile
        if self.player_one_moves:
            computer_move = self.find_winning_move(self.player_one_moves)
            if computer_move:
                self.change_state(pos=computer_move, turn=2)
                return

        # If no-one is one move from winning, take the center if possible; otherwise play a random move
        if not computer_move:
            if (1, 1) in self.open_spaces:
                computer_move = [1, 1]
            else:
                move_bank = [pos for pos in OUTER_POSITIONS if pos in self.open_spaces]
                computer_move = random_choice(move_bank)

        # Change the value of the selected space
        self.change_state(pos=computer_move, turn=2)

    def update_open_spaces(self) -> None:
        """Updates open_spaces variable."""
        new_open_spaces: list = []

        # Loop through all spaces and append to new_open_spaces if the space is open
        for row_num, row in enumerate(self.board):
            for col_num, value in enumerate(row):
                if value == '-':
                    new_open_spaces.append((row_num, col_num))

        # Assign open_spaces to new_open_spaces
        self.open_spaces = new_open_spaces

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

        # Define player characters (Possibly allow players to pick their characters in the future?)
        self.player_one_char = "X"
        self.player_two_char = "O"

        while self.game_running:
            self.display_board()

            # Check if player one wins or draws
            if not self.player_turn(1):
                continue

            if self.check_for_win():
                break

            # Check if player two / computer wins or draws
            if self.is_two_player == 'y':
                self.display_board()
                self.player_turn(2)
            else:
                self.computer_turn()

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


if __name__ == "__main__":
    controller: Controller = Controller()
    play_again: bool = controller.play_round()

    while play_again:
        play_again = controller.play_round()
