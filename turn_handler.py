from random import choice as random_choice


class TurnHandler:
    def __init__(self, board: list, win_pos: tuple):
        # Initialize board
        self.board: list = board
        self.open_spaces: list = []
        self.update_open_spaces()

        # Per-round data
        self.player_one_moves: list = []
        self.player_two_moves: list = []

        # Initialize constants
        self.ALLOWED_NUMBERS: tuple = 1, 2, 3
        self.OUTER_POSITIONS: tuple = (0, 1), (1, 0), (1, 2), (2, 1), (0, 0), (0, 2), (2, 0), (2, 2)
        self.WINNING_POSITIONS: tuple = win_pos

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
        filtered_coords: tuple = tuple([item for item in semifiltered_coords if item + 1 in self.ALLOWED_NUMBERS])
        print(filtered_coords)

        # Check if numbers above 3 were entered
        if not len(filtered_coords) == 2:
            print('\n>>>> Please only enter the numbers 1, 2, or 3 <<<<')
            return False

        if not self.change_state(pos=(filtered_coords[0], filtered_coords[1]), turn=player):
            print("\n>>>> Please enter a valid set of coordinates. <<<<")
            return False

        return True

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
                move_bank = [pos for pos in self.OUTER_POSITIONS if pos in self.open_spaces]
                computer_move = random_choice(move_bank)

        # Change the value of the selected space
        self.change_state(pos=computer_move, turn=2)

    def find_winning_move(self, moves: tuple | list) -> list:
        """Returns any move that wins in 1 turn for a given list of moves that have already been made."""
        # Loop through all winning configurations and check if two of the moves are already played by one person.
        # Also, check if the final missing space is open or blocked. If it is open, return the final missing space.
        for config in self.WINNING_POSITIONS:
            if config[0] in moves and config[1] in moves and config[2] in self.open_spaces:
                return config[2]
            if config[0] in moves and config[2] in moves and config[1] in self.open_spaces:
                return config[1]
            if config[1] in moves and config[2] in moves and config[0] in self.open_spaces:
                return config[0]
        return []

    def change_state(self, pos: tuple | list, turn: int) -> bool:
        """Changes a position at a given tile if the tile is blank, i.e. has a value of '-'. Returns boolean based on
        whether the tile was empty or not."""
        # Check if chosen tile is empty
        if not self.board[pos[0]][pos[1]] == '-':
            return False

        # Change the tile to the given player's tile character and append to the given player's list of played moves
        match turn:
            case 1:
                self.board[pos[0]][pos[1]] = 'X'
                self.player_one_moves.append(tuple(pos))
            case 2:
                self.board[pos[0]][pos[1]] = 'O'
                self.player_two_moves.append(tuple(pos))

        # Update the list of open spaces to exclude the played move
        self.update_open_spaces()
        return True

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
