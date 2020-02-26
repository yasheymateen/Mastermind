"""Definition of the Board class used in the Mastermind project."""

class Board(object):

    """Mastermind Board class."""

    def __init__(self, pattern_length, screen_width, turns):
        self.pattern_length = pattern_length
        self.screen_width = screen_width

        # Initialise board

        self.board = []
        board_row = self.__create_row("|", " ")
        board_end = self.__create_row("+", "-")

        self.board.append(board_end)
        for row in range(turns * 2 + 1):
            self.board.append(board_row)
        self.board.append(board_end)


    def __create_row(self, border, slot):
        """Return board row with given border and slot symbols."""
        return (" " * (self.screen_width / 4)) + border + \
                (slot * (self.pattern_length * 3 + 2)) + border + \
                (slot * (self.pattern_length * 2 + 1)) + border


    def display(self):
        """Display board."""
        print '\n'.join(self.board) + '\n'


    def update(self, turn, guess, feedback):
        """Update board with given guess and feedback at turn."""
        board_row = (" " * (self.screen_width / 4)) + "|  "
        for colour in guess:
            board_row += colour + "  "          # Add guess
        board_row += "| "
        for key in feedback:
            board_row += key + " "              # Add feedback
        for empty_key in range(self.pattern_length - len(feedback)):
            board_row += "  "                   # Add empty slots
        board_row += "|"
        self.board[(turn + 1) * 2] = board_row  # Update board row
