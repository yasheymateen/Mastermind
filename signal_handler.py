"""Definition of the signal handler used in the Mastermind project."""

import os
import sys

def quit_game(signal, frame):
    """Quit the game if Ctrl-C is pressed."""
    os.system('clear')
    print "Thank you for playing!"
    sys.exit()
