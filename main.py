# TODO: Add winstreak functionality by implementing restart/retry option
from random import choice as random_choice

ALLOWED_NUMBERS: tuple = ('1', '2', '3')
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

OUTER_POSITIONS: tuple = ((0, 1), (1, 0), (1, 2), (2, 1), (0, 0), (0, 2), (2, 0), (2, 2))


class Controller:
    def __init__(self):
        # Create board
        self.board: list = [['-' for _ in range(3)] for _ in range(3)]
        self.open_spaces: list = []
        self.update_open_spaces()

        self.winner: int = 0
        self.player_one_moves: list = []
        self.player_two_moves: list = []
        self.player_one_char: str = ''
        self.player_two_char: str = ''
        self.player_one_winstreak, self.player_two_winstreak = 0, 0

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
        return False

    def change_state(self, pos: tuple | list, state: int, turn: int) -> bool:
        """Changes a position at a given tile if the tile is blank, i.e. has a value of '-'. Returns boolean based on
        whether the tile was empty or not."""
        # Check if chosen tile is empty
        if not self.board[pos[0]][pos[1]] == '-':
            return False

        # Change tile
        match state:
            case 1:
                self.board[pos[0]][pos[1]] = self.player_one_char
            case 2:
                self.board[pos[0]][pos[1]] = self.player_two_char

        match turn:
            case 1:
                self.player_one_moves.append(tuple(pos))
            case 2:
                self.player_two_moves.append(tuple(pos))
        controller.update_open_spaces()
        return True

    def player_turn(self, player: int) -> bool:
        """Changes a tile on the board to player_one_char at position that player specifies. Returns boolean based on if
        the change was successful, i.e. valid coordinates were given. """
        player_moves: str = input('Enter a row and a column (Separation is optional): ')

        unfiltered_coords: tuple = tuple([move for move in player_moves])
        filtered_coords: tuple = tuple([int(item) - 1 for item in unfiltered_coords if item in ALLOWED_NUMBERS])

        tile_empty: bool = self.change_state(pos=(filtered_coords[0], filtered_coords[1]), state=player, turn=player)

        # Check if coordinates are the right length and not on an already chosen tile
        if not len(filtered_coords) == 2 or not tile_empty:
            print("\n>>>> Please enter a valid set of coordinates. <<<<")
            return False

        return True

    def find_winning_move(self, moves: tuple | list) -> list:
        """Returns any move that wins in 1 turn for a given list of moves that have already been made."""
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
            self.change_state(pos=computer_move, state=2, turn=2)
            return

        # If player is 1 move from winning, make move in winning tile
        if self.player_one_moves:
            computer_move = self.find_winning_move(self.player_one_moves)
            if computer_move:
                self.change_state(pos=computer_move, state=2, turn=2)
                return

        # If player not 1 move away from winning, take the center or play random move
        if not computer_move:
            if (1, 1) in self.open_spaces:
                computer_move = [1, 1]
            else:
                move_bank = [pos for pos in OUTER_POSITIONS if pos in self.open_spaces]
                computer_move = random_choice(move_bank)

        self.change_state(pos=computer_move, state=2, turn=2)

    def update_open_spaces(self) -> None:
        """Updates open_spaces variable."""
        new_open_spaces: list = []

        for row_num, row in enumerate(self.board):
            for col_num, value in enumerate(row):
                if value == '-':
                    new_open_spaces.append((row_num, col_num))

        self.open_spaces = new_open_spaces

    def display_board(self) -> None:
        """Prints board to console."""
        for row in self.board:
            display_str: str = ''
            for item in row:
                display_str += f'{item} '
            print(display_str)


controller: Controller = Controller()
game_running: bool = True
is_two_player: str = input('Do you want to play a two-player game? Enter "y/n": ')

while not is_two_player == 'y' and not is_two_player == 'n':
    is_two_player = input('Please enter "y/n": ')

# controller.player_one_char = input("What should player one's tiles look like?: ")
# controller.player_two_char = input("What should the player two's tiles look like?: ")
controller.player_one_char = "X"
controller.player_two_char = "O"

while game_running:
    controller.display_board()

    # Check if player one wins or draws
    if not controller.player_turn(1):
        continue

    if controller.check_for_win():
        break

    # Check if player two / computer wins or draws
    if is_two_player == 'y':
        controller.display_board()
        controller.player_turn(2)
    else:
        controller.computer_turn()

    if controller.check_for_win():
        break

match controller.winner:
    case 1:
        print(f"Winning streak: {controller.player_one_winstreak}")
    case 2:
        print(f"Winning streak: {controller.player_two_winstreak}")
