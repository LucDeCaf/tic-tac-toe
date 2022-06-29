from random import choice

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
        self.board: list = [['-' for _ in range(3)] for _ in range(3)]
        self.open_spaces: list = []
        self.player_moves: list = []
        self.computer_moves: list = []
        self.player_char: str = ""
        self.computer_char: str = ""
        self.update_open_spaces()

    def check_for_win(self) -> int:
        """Returns integer based on if there is a win, loss, draw, or nothing; Returns 0: Nothing, 1: Player,
        2: Computer, 3: Draw"""
        if not self.open_spaces:
            return 3
        for pos in WINNING_POSITIONS:
            if pos[0] in self.player_moves and pos[1] in self.player_moves and pos[2] in self.player_moves:
                return 1
            if pos[0] in self.computer_moves and pos[1] in self.computer_moves and pos[2] in self.computer_moves:
                return 2
        return 0

    def change_state(self, pos: tuple | list, state: int, turn: int) -> bool:
        """Changes a position at a given tile if the tile is blank, i.e. has a value of '-'. Returns boolean based on
        whether the tile was empty or not."""
        # Check if chosen tile is empty
        if not self.board[pos[0]][pos[1]] == '-':
            return False

        # Change tile
        match state:
            case 0:
                self.board[pos[0]][pos[1]] = '-'
            case 1:
                self.board[pos[0]][pos[1]] = self.player_char
            case 2:
                self.board[pos[0]][pos[1]] = self.computer_char

        match turn:
            case 1:
                self.player_moves.append(tuple(pos))
            case 2:
                self.computer_moves.append(tuple(pos))
        return True

    def player_turn(self) -> bool:
        """Changes a tile on the board to player_char at position that player specifies. Returns boolean based on if the
        change was successful, i.e. valid coordinates were given."""
        player_moves: str = input('Enter a row and a column (Separation is optional): ')
        unfiltered_coords: tuple = tuple([move for move in player_moves])

        filtered_coords: tuple = tuple([int(item) - 1 for item in unfiltered_coords if item in ALLOWED_NUMBERS])

        if not len(filtered_coords) == 2 or not self.change_state(
                pos=(filtered_coords[0], filtered_coords[1]), state=1, turn=1):
            print("\n>>>> Please enter a valid set of coordinates. <<<<")
            return False

        return True

    def find_winning_move(self, moves) -> list:
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
        """Changes tile on board to computer_char at semi-random position."""
        # If computer can win in 1 move, play move in winning tile
        computer_move: list = self.find_winning_move(self.computer_moves)
        if computer_move:
            self.change_state(pos=computer_move, state=2, turn=2)
            return

        # If player is 1 move from winning, make move in winning tile
        if self.player_moves:
            computer_move = self.find_winning_move(self.player_moves)
            if computer_move:
                self.change_state(pos=computer_move, state=2, turn=2)
                return

        # If player not 1 move away from winning, take the center or play random move
        if not computer_move:
            if (1, 1) in self.open_spaces:
                computer_move = [1, 1]
            else:
                move_bank = [pos for pos in OUTER_POSITIONS if pos in self.open_spaces]
                computer_move = choice(move_bank)

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
player_won: bool = False

# controller.player_char = input("What do you want your tiles to look like?: ")
# controller.computer_char = input("What should the computer's tiles look like?: ")
controller.player_char = "X"
controller.computer_char = "O"

while game_running:
    controller.display_board()

    # Check if player wins or draws
    if not controller.player_turn():
        continue

    controller.update_open_spaces()

    match controller.check_for_win():
        case 1:
            controller.display_board()
            print('\n>>> Player wins! <<<')
            player_won = True
            break
        case 3:
            controller.display_board()
            print('\n>>> Draw. <<<')
            break

    # Check if computer wins
    controller.computer_turn()

    controller.update_open_spaces()

    match controller.check_for_win():
        case 2:
            controller.display_board()
            print('\n>>> Computer wins! <<<')
            break
        case 3:
            controller.display_board()
            print('\n>>> Draw. <<<')
            break

with open("winstreak.csv", 'r') as datafile:
    try:
        total_wins = int(datafile.read())
    except ValueError:
        total_wins = 0

if player_won:
    total_wins += 1

    with open("winstreak.csv", "w") as datafile:
        datafile.write(str(total_wins))

print(f"Total wins: {total_wins}")
